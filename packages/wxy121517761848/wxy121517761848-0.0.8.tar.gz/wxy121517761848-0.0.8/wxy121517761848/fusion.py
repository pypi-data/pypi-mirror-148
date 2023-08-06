"""Main Fusion module."""

import datetime
import json
import logging
import re
import sys
from datetime import timedelta
from pathlib import Path
from typing import Union

import pandas as pd
import requests
from tabulate import tabulate

DT_YYYYMMDD_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})$")
DT_YYYY_MM_DD_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
OAUTH_GRANT_TYPE = 'client_credentials'
DEFAULT_CHUNK_SIZE = 2**16
DEFAULT_PARALLELISM = 5
HTTP_SUCCESS = 200
USER_AGENT = 'Mozilla/5.0'
CONTENT_TYPE = 'application/x-www-form-urlencoded'

logger = logging.getLogger(__name__)
VERBOSE_LVL = 25


class APIRequestError(Exception):
    """APIRequestError exception wrapper.

    Args:
        Exception : Exception to wrap.
    """

    pass


class APIResponseError(Exception):
    """APIResponseError exception wrapper.

    Args:
        Exception : Exception to wrap.
    """

    pass


class APIConnectError(Exception):
    """APIConnectError exception wrapper.

    Args:
        Exception : Exception to wrap.
    """

    pass


class UnrecognizedFormatError(Exception):
    """UnrecognizedFormatError exception wrapper.

    Args:
        Exception : Exception to wrap.
    """

    pass


class CredentialError(Exception):
    """CredentialError exception wrapper.

    Args:
        Exception : Exception to wrap.
    """

    pass


def _res_plural(ref_int: int, pluraliser: str = 's') -> str:
    return '' if ref_int == 1 else pluraliser


def _is_json(data) -> bool:
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def _normalise_dt_param(dt: Union[str, int, datetime.datetime, datetime.date]) -> str:

    if isinstance(dt, (datetime.date, datetime.datetime)):
        return dt.strftime("%Y-%m-%d")

    if isinstance(dt, int):
        dt = str(dt)

    matches = DT_YYYYMMDD_RE.match(dt)

    if matches:
        return "-".join(matches.groups())

    raise ValueError(f"{dt} is not in a recognised data format")


def _normalise_dt_param_str(dt: str) -> tuple:

    date_parts = dt.split(":")

    if not date_parts or len(date_parts) > 2:
        raise ValueError(f"Unable to parse {dt} as either a date or an interval")

    return tuple((_normalise_dt_param(dt_part) if dt_part else dt_part for dt_part in date_parts))


def __distribution_to_filename(
    root_folder: str, dataset: str, datasetseries: str, file_format: str, catalog: str = 'common'
) -> Path:
    if datasetseries[-1] == '/' or datasetseries[-1] == '\\':
        datasetseries = datasetseries[0:-1]
    file_name = f"{dataset}__{catalog}__{datasetseries}.{file_format}"
    return Path(root_folder, file_name)


def _filename_to_distribution(file_name: str) -> tuple:
    dataset, catalog, series_format = Path(file_name).name.split('__')
    datasetseries, file_format = series_format.split('.')
    return (catalog, dataset, datasetseries, file_format)


def _distribution_to_url(
    root_url: str, dataset: str, datasetseries: str, file_format: str, catalog: str = 'common'
) -> str:
    if datasetseries[-1] == '/' or datasetseries[-1] == '\\':
        datasetseries = datasetseries[0:1]
    return f"{root_url}catalogs/{catalog}/datasets/{dataset}/{datasetseries}/distributions/{file_format}"


class FusionCredentials:
    """Class to manage Fusion Creds and OAuth."""

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        resource: str = None,
        auth_url: str = None,
        proxies: str = None,
    ) -> None:
        """Constuctor for Creds mgr.

        Args:
            client_id (str, optional): Client ID as provided by Fusion. Defaults to None.
            client_secret (str, optional): Client Secret as provided by Fusion. Defaults to None.
            resource (str, optional): Fusion resource ID as provided by Fusion. Defaults to None.
            auth_url (str, optional): Auth URL as provided by Fusion. Defaults to None.
            proxies (str, optional): Any proxy servers to hop through. Defaults to None.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.resource = resource
        self.auth_url = auth_url
        self.proxies = proxies

    @staticmethod
    def generate_credentials_file(
        credentials_file: str = 'config/client_credentials.json',
        client_id: str = None,
        client_secret: str = None,
        resource: str = None,
        auth_url: str = None,
        proxies: str = None,
    ):
        """_summary_.

        Args:
            credentials_file (str, optional): _description_. Defaults to 'config/client_credentials.json'.
            client_id (str, optional): _description_. Defaults to None.
            client_secret (str, optional): _description_. Defaults to None.
            resource (str, optional): _description_. Defaults to None.
            auth_url (str, optional): _description_. Defaults to None.
            proxies (str, optional): _description_. Defaults to None.

        Raises:
            CredentialError: Exception describing creds issue

        Returns:
            _type_: _description_
        """
        if not client_id:
            raise CredentialError('A valid client_id is required')
        if not client_secret:
            raise CredentialError('A valid client secret is required')
        if not resource:
            raise CredentialError('A valid resource is required')
        if not auth_url:
            raise CredentialError('A valid authentication server URL is required')

        data = dict(
            {'client_id': client_id, 'client_secret': client_secret, 'resource': resource, 'auth_url': auth_url}
        )

        if proxies:
            data['proxies'] = proxies
        json_data = json.dumps(data)

        with open(credentials_file, 'w') as credentialsfile:
            credentialsfile.write(json_data)

        credentials = FusionCredentials(client_id, client_secret, resource, auth_url)
        return credentials

    @staticmethod
    def from_dict(credentials: dict):
        """Create Creds object from dict.

        Args:
            credentials (dict): conforming dictionary with creds attributes

        Returns:
            FusionCredentials: creds object
        """
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']
        resource = credentials['resource']
        auth_url = credentials['auth_url']
        proxies = credentials.get('proxies')
        creds = FusionCredentials(client_id, client_secret, resource, auth_url, proxies)
        return creds

    @staticmethod
    def from_file(credentials_file: str = 'config/client.credentials.json'):
        """_summary_.

        Args:
            credentials_file (str, optional): _description_. Defaults to 'config/client.credentials.json'.

        Returns:
            _type_: _description_
        """
        with open(credentials_file, 'r') as credentials:
            data = json.load(credentials)
            credentials = FusionCredentials.from_dict(data)
            return credentials

    @staticmethod
    def from_object(credentials_source: Union[str, dict]):
        """_summary_.

        Args:
            credentials_source (Union[str, dict]): _description_

        Raises:
            CredentialError: _description_

        Returns:
            _type_: _description_
        """
        if isinstance(credentials_source, dict):
            return FusionCredentials.from_dict(credentials_source)
        elif isinstance(credentials_source, str):
            if _is_json(credentials_source):
                return FusionCredentials.from_dict(json.loads(credentials_source))
            else:
                return FusionCredentials.from_file(credentials_source)

        raise CredentialError(f'Could not resolve the credentials provided: {credentials_source}')


class FusionOAuthAdapter(requests.adapters.HTTPAdapter):
    """Fusion OAuth model specific requests adapter."""

    def __init__(self, credentials, proxies={}, refresh_within_seconds=5, *args, **kwargs) -> None:
        """_summary_.

        Args:
            credentials (_type_): _description_
            proxies (dict, optional): _description_. Defaults to {}.
            refresh_within_seconds (int, optional): _description_. Defaults to 5.
        """
        super(FusionOAuthAdapter, self).__init__(*args, **kwargs)

        if isinstance(credentials, FusionCredentials):
            self.credentials = credentials
        else:
            self.credentials = FusionCredentials.from_object(credentials)

        if proxies:
            self.proxies = proxies
        else:
            self.proxies = self.credentials.proxies

        self.bearer_token_expiry = datetime.datetime.now()
        self.number_token_refreshes = 0
        self.refresh_within_seconds = refresh_within_seconds

    def send(self, request, **kwargs):
        """_summary_.

        Args:
            request (_type_): _description_
        """

        def _refresh_token_data():
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.credentials.client_id,
                "client_secret": self.credentials.client_secret,
                "aud": self.credentials.resource,
            }

            try:
                response = requests.Session().post(self.credentials.auth_url, data=payload)
                response_data = response.json()
                access_token = response_data["access_token"]
                expiry = response_data["expires_in"]
                return access_token, expiry
            except Exception as ex:
                raise Exception(f'Failed to authenticate against OAuth server {ex}')

        token_expires_in = (self.bearer_token_expiry - datetime.datetime.now()).total_seconds()
        if token_expires_in < self.refresh_within_seconds:
            token, expiry = _refresh_token_data()
            self.token = token
            self.bearer_token_expiry = datetime.datetime.now() + timedelta(seconds=int(expiry))
            self.number_token_refreshes += 1
            logger.log(
                VERBOSE_LVL,
                f'Refreshed token {self.number_token_refreshes} time{_res_plural(self.number_token_refreshes)}',
            )

        # url = urlparse(request.url)
        request.headers.update({'Authorization': f'Bearer {self.token}', 'jpmc-token-provider': 'authe'})
        response = super(FusionOAuthAdapter, self).send(request, **kwargs)
        return response


def _get_session(credentials):
    session = requests.Session()
    auth_handler = FusionOAuthAdapter(credentials)
    if credentials.proxies:
        session.proxies.update(credentials.proxies)
    session.mount("https://", auth_handler)
    return session


def _stream_single_file_new_session_dry_run(credentials, url: str, output_file: str):
    try:
        _get_session(credentials).head(url)
        return (True, output_file, None)
    except Exception as ex:
        return (False, output_file, ex)


def _stream_single_file_new_session(
    credentials,
    url: str,
    output_file: str,
    overwrite: bool = True,
    block_size=DEFAULT_CHUNK_SIZE,
    dry_run: bool = False,
):
    if dry_run:
        return _stream_single_file_new_session_dry_run(credentials, url, output_file)

    if not overwrite and Path(output_file).exists():
        return (True, output_file, None)

    try:
        with _get_session(credentials).get(url, stream=True) as r:
            with open(output_file, "wb") as outfile:
                for chunk in r.iter_content(block_size):
                    outfile.write(chunk)
        return (True, output_file, None)
    except Exception as ex:
        return (False, output_file, ex)


def _stream_single_file(session, url: str, output_file: str, blocl_size=DEFAULT_CHUNK_SIZE):
    with session.get(url, stream=True) as r:
        with open(output_file, "wb") as outfile:
            for chunk in r.iter_content(blocl_size):
                outfile.write(chunk)


class Fusion:
    """Core Fusion class."""

    def __init__(
        self,
        credentials: Union[str, dict] = 'config/client_credentials.json',
        root_url: str = "https://fusion-api.jpmorgan.com/fusion/v1/",
        download_folder: str = "downloads",
        log_level: int = logging.ERROR,
    ) -> None:
        """_summary_.

        Args:
            credentials (Union[str, dict], optional): _description_. Defaults to 'config/client_credentials.json'.
            root_url (_type_, optional): _description_. Defaults to "https://fusion-api.jpmorgan.com/fusion/v1/".
            download_folder (str, optional): _description_. Defaults to "downloads".
            log_level (int, optional): _description_. Defaults to logging.ERROR.
        """
        self.root_url = root_url
        self.download_folder = download_folder
        Path(download_folder).mkdir(parents=True, exist_ok=True)

        if logger.hasHandlers():
            logger.handlers.clear()
        file_handler = logging.FileHandler(filename="fusion_sdk.log")
        logging.addLevelName(VERBOSE_LVL, "VERBOSE")
        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(name)s:%(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
        logger.addHandler(file_handler)
        logger.setLevel(log_level)

        if isinstance(credentials, FusionCredentials):
            self.credentials = credentials
        else:
            self.credentials = FusionCredentials.from_object(credentials)

        self.session = _get_session(self.credentials)

    def __call_for_dataframe(self, url: str) -> pd.DataFrame:

        # data = self.session.get(url)
        # Had to return something to calm the linter
        return pd.DataFrame()

    def list_catalogs(self, output: bool = False) -> Union[None, pd.DataFrame]:
        """_summary_.

        Args:
            output (bool, optional): _description_. Defaults to False.

        Returns:
            Union[None, pd.DataFrame]: _description_
        """
        url = f'{self.root_url}catalogs/'
        response = self.session.get(url)
        response.raise_for_status()
        table = response.json()['resources']
        df = pd.DataFrame(table).reset_index(drop=True)

        if output:
            print(tabulate(df, headers="keys", tablefmt="psql"))
            return None
        else:
            return df

    def catalog_resources(self, catalog: str = 'common', output: bool = False) -> Union[None, pd.DataFrame]:
        """_summary_.

        Args:
            catalog (str, optional): _description_. Defaults to 'common'.
            output (bool, optional): _description_. Defaults to False.

        Returns:
            Union[None, pd.DataFrame]: _description_
        """
        url = f'{self.root_url}catalogs/{catalog}'
        response = self.session.get(url)
        response.raise_for_status()
        table = response.json()['resources']
        df = pd.DataFrame(table).reset_index(drop=True)

        if output:
            print(tabulate(df, headers="keys", tablefmt="psql"))
            return None
        else:
            return df

    def list_products(
        self, contains: Union[str, list] = None, catalog: str = 'common', output: bool = False, max_results: int = -1
    ) -> Union[None, pd.DataFrame]:
        """_summary_.

        Args:
            contains (Union[str, list], optional): _description_. Defaults to None.
            catalog (str, optional): _description_. Defaults to 'common'.
            output (bool, optional): _description_. Defaults to False.
            max_results (int, optional): _description_. Defaults to -1.

        Returns:
            Union[None, pd.DataFrame]: _description_
        """
        url = f'{self.root_url}catalogs/{catalog}/products'
        response = self.session.get(url)
        response.raise_for_status()
        table = response.json()['resources']
        df = pd.DataFrame(table).reset_index(drop=True)

        if contains:
            if isinstance(contains, list):
                contains = "|".join(f'{s}' for s in contains)
            df = df[df['identifer'].str.contains(contains)]

        df = df[0:max_results]

        if output:
            print(tabulate(df, headers="keys", tablefmt="psql"))
            return None
        else:
            return df

    def list_datasets(
        self, contains: Union[str, list] = None, catalog: str = 'common', output: bool = False, max_results: int = -1
    ) -> Union[None, pd.DataFrame]:
        """_summary_.

        Args:
            contains (Union[str, list], optional): _description_. Defaults to None.
            catalog (str, optional): _description_. Defaults to 'common'.
            output (bool, optional): _description_. Defaults to False.
            max_results (int, optional): _description_. Defaults to -1.

        Returns:
            Union[None, pd.DataFrame]: _description_
        """
        url = f'{self.root_url}catalogs/{catalog}/datasets'
        response = self.session.get(url)
        response.raise_for_status()
        table = response.json()['resources']
        df = pd.DataFrame(table).reset_index(drop=True)

        if contains:
            if isinstance(contains, list):
                contains = "|".join(f'{s}' for s in contains)
            df = df[df['identifer'].str.contains(contains)]

        df = df[0:max_results]

        if output:
            print(tabulate(df, headers="keys", tablefmt="psql"))
            return None
        else:
            return df
