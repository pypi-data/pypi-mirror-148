import io
import json
import logging
from typing import Dict
from typing import List
from typing import Union

import requests
from requests.adapters import HTTPAdapter
import pandas as pd
from urllib.error import HTTPError
from urllib3 import Retry


class AhrefsClient:
    """ Client for interacting with ahrefs API.

    Attributes:
        session (requests.Session): Session object for handling the connection to ahrefs.
        logger (logging.Logger): Logger for logging the object's method calls.
    """

    # URLs for ahrefs requests
    _APP_BASE_URL = 'https://app.ahrefs.com'
    _AUTH_BASE_URL = 'https://auth.ahrefs.com'
    _LOGIN_URL = _AUTH_BASE_URL + '/auth/login'
    _UPDATE_SERP_URL = _APP_BASE_URL + '/v4/keUpdate'
    _KEYWORD_EXPORT_URL = _APP_BASE_URL + '/v4/keListOverviewExport?mode=csv-utf8'
    _SERP_EXPORT_URL = _APP_BASE_URL + '/v4/keListOverviewSerpsExport?mode=csv-utf8'

    # Column names used in csv exports
    _KEYWORD_COLUMN_NAME = 'Keyword'

    def __init__(self, email: str, password: str):
        """ Sets up a session to ahrefs given the specified credentials.

        Args:
            email: The e-mail used to log in.
            password: The password used with <email> to log in.
        """
        self._email = email
        self._password = password
        self.session = requests.Session()
        self.session.auth = (self._email, self._password)
        self.session.mount('https://', self._retry_adapter(retries=3, backoff_factor=4))
        self.logger = logging.getLogger(__name__)
        # Log in and attach the cookies from the response to session
        login_response = self._request(method='POST', url=self._LOGIN_URL,
                                       data=self._build_login_body())
        self.session.cookies = login_response.cookies

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.session.__exit__()

    def __del__(self):
        self.session.__exit__()

    @staticmethod
    def _retry_adapter(
            retries=5,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 501, 502, 503, 504)
    ):
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        return HTTPAdapter(max_retries=retry)

    def _request(self, method: str = 'GET', url: str = None, *args, **kwargs):
        """ Wrapper around the session.request method that handles HTTP errors

        Args:
            method: The HTTP/HTTPS request method. I.e. GET or POST.
            url: The URL to perform the request on.

        Returns:
            A requests.Response object with the request response.

        Raises:
            An HTTPError with the response status code and failure reason if the status code
                response is not 200.
        """
        response = self.session.request(method, url, *args, **kwargs)
        if response.status_code != 200:
            raise HTTPError(url, response.status_code, response.reason, None, None)
        return response

    def _build_login_body(self):
        """ Bulds the body of the message for the request to the login page. """
        return json.dumps(
            {
                'remember_me': True,
                'auth': {
                    'password': self._password,
                    'login': self._email
                }
            }
        )

    def _build_keyword_update_body(self, country_abbr: str, keyword_list: List[str]):
        """ Builds the body of the message for the request for updating the keywords. """
        return json.dumps({'country': country_abbr, 'keywords': keyword_list})

    def _build_keyword_export_body(self, country_abbr: str, list_id: int, keyword_no: int) -> str:
        """ Builds the body of the message for the request for exporting the keywords/SERP data. """
        return json.dumps(
            {
                "limit": keyword_no,
                "offset": 0,
                "filters": self._build_default_filters(),
                "sort": {"order": "Desc", "by": "Volume"},
                "country": country_abbr,
                "searchEngine": "Google",
                "listId": list_id
            }
        )

    def _build_default_filters(self) -> List[Dict[str, Union[List[str], str]]]:
        """ Builds a list of the default filters that are used in exporting keyword/SERP data. """
        return [
            {"filter": ["Range", "None"], "id": "Difficulty"},
            {"filter": ["Range", "None"], "id": "Volume"},
            {"filter": ["Range", "None"], "id": "GlobalVolume"},
            {"filter": ["Range", "None"], "id": "TrafficPotential"},
            {"filter": ["Terms", "None"], "id": "Terms"},
            {"filter": ["ParentTopic", "None"], "id": "ParentTopic"},
            {"filter": ["Range", "None"], "id": "WordCount"},
            {"filter": ["SerpFeatures", "None"], "id": "Serp"},
            {"filter": ["IncludeWords", "None"], "id": "Include"},
            {"filter": ["ExcludeWords", "None"], "id": "Exclude"},
            {"filter": ["Range", "None"], "id": "CPS"},
            {"filter": ["UsdRange", "None"], "id": "CPC"}
        ]

    def _build_keyword_export_url(self, include_serps: bool):
        """ Builds the URL used for exporting keyword/SERP data. """
        return self._SERP_EXPORT_URL if include_serps else self._KEYWORD_EXPORT_URL

    def export_keyword_list(
            self,
            country_abbr: str,
            list_id: int,
            keyword_no: int = 5000,
            csv_path: str = 'keyword_export.csv',
            include_serps=False
    ) -> List[str]:
        """ Exports a csv with keyword/SERP data.

        Args:
            country_abbr: The abbreviation of the country to export data for. E.g. 'us' or 'se'.
            list_id: The id of the keyword list to extract data from.
            keyword_no: The number of keywords to extract data for.
            csv_path: The path to the csv where the data should be written to. The file is overwrit-
                ten if it already exists.
            include_serps: Whether to include SERP data in the export. This is the same with the
                include_serps option in the ahrefs browser API.

        Returns:
            A list of strings corresponding to the keywords we exported data for.
        """
        # Request exported data
        response = self._request(
            method='POST',
            url=self._build_keyword_export_url(include_serps),
            data=self._build_keyword_export_body(
                country_abbr=country_abbr, list_id=list_id, keyword_no=keyword_no
            ),
            headers={'Content-type': 'application/json; charset=UTF-8'}
        )
        # Read response data into dataframe
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        # Write out dataframe into csv file
        df.to_csv(csv_path)
        # Return keywords
        return df[self._KEYWORD_COLUMN_NAME]

    def update_keywords(self, country_abbr: str, keyword_list: List[str]):
        self._request(
            method='POST',
            url=self._UPDATE_SERP_URL,
            data=self._build_keyword_update_body(country_abbr=country_abbr,
                                                 keyword_list=keyword_list),
            headers={'Content-type': 'application/json; charset=UTF-8'}
        )

    def update_keywords_for_countries(self, country_abbr_list: List[str], keyword_list=List[str]):
        for country in country_abbr_list:
            try:
                self.update_keywords(country_abbr=country, keyword_list=keyword_list)
            except HTTPError as e:
                self.logger.exception(e)
