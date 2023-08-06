import datetime
from urllib.parse import urljoin
import warnings
import pandas as pd
import requests
from requests import get

# ttest


class API:
    """_summary_

    This class is used to interact with the API
    """

    def __init__(self, api_root, username, password):

        self.api_root = api_root
        self.username = username
        self._password = password
        self.access_token = None
        self.refresh_token = None
        self.__get_tokens()  # get the tokens
        self._groups = None

    @property
    def __get_header(self):
        formatted_token = f"Bearer {self.access_token}"
        return {"Authorization": formatted_token}

    def query(self, dt: tuple, location: str, metrics: list):
        """
        Run a query for metrics on the OWI DATA API

        :param dt: Start and end timestamp of the data to be processed
        :type dt: tuple of datetime.datetime objects
        :param location: String of a valid location for which the data is to be obtained
        :type location: str
        :param metrics: List of valid metrics to pass to the database
        :type metrics: list
        :returns: Dataframe with all results
        :rtype: pd.DataFrame
        """
        if not isinstance(dt, tuple):
            raise TypeError(
                "Timestamps should be passed into query as a tuple of two timestamps"
            )

        if dt[0] > dt[1]:
            raise ValueError(
                " ".join(
                    [
                        "Timestamp",
                        str(dt[0]),
                        "predates",
                        str(dt[1]),
                        ". Check your timestamps and assure they are in the right order",
                    ]
                )
            )

        params = {
            "metric": metrics,
            "location": location,
            "startdatetime": _parse_timestamps(dt[0]),
            "enddatetime": _parse_timestamps(dt[1]),
        }

        resp = self._run_request(url="query", params=params)

        location = list(resp.json().keys())[0]

        df = pd.json_normalize(resp.json()[location], max_level=0)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)
        return df

    @property
    def groups(self):
        """
        Query all the groups the current user has been granted access to

        :return: Dataframe containing the groups the user has access to
        :rtype: pd.DataFrame
        """
        if self._groups is not None:
            return self._groups

        resp = self._run_request("mygroups")
        if resp:
            json_dict = resp.json()
            for k in json_dict.keys():
                json_dict[k].update({"id": k})

            json_list = [json_dict[k] for k in json_dict.keys()]

            df = pd.json_normalize(json_list).set_index("id")
            self._groups = df
            return df

        return None

    def metrics(self, locations, datagroups=None):
        """
        Query the available parameters for a given location.

        :param locations: Location (str, e.g. BBC01) or a list of locations
        :type locations: str or list
        :param datagroups: datagroup (str, e.g. scada) or a list of datagroups
        :type datagroups: str or list
        :return: Dataframe with the available metrics for a given location
        :rtype: pd.DataFrame
        """
        params = {"location": locations}
        if datagroups:
            params["datagroup"] = datagroups

        resp = self._run_request("metrics", params=params)
        metrics = None
        if resp:
            json_dict = resp.json()
            # Quickly add the location to each row
            df_list = []
            for k in json_dict.keys():
                if json_dict.get(k) != "":
                    df_location = pd.json_normalize(json_dict[k])
                    df_location["location"] = k
                    df_list.append(df_location)
                    metrics = pd.concat(df_list)

        return metrics

    def _run_request(self, url: str, params=None):
        """
        Simplify the handling of requests. No need to specify the root url and authentication

        :param url: URL (below root) for the query to run on
        :type url: string
        :param params: List of suitabl, metrics, defaults to None
        :type params: list, optional
        """
        resp = get(
            url=urljoin(self.api_root, url), params=params, headers=self.__get_header
        )

        if resp.status_code == 200:
            return resp
        if resp.status_code == 401:
            self.__token_verif_and_renew()
            resp = get(
                url=urljoin(self.api_root, url),
                params=params,
                headers=self.__get_header,
            )
            return resp
        if resp.status_code == 502:
            warnings.warn(
                f"Failed query ({str(resp.status_code)}) : TIP: try again with less data {str(resp.url)}"
            )
            return None

        warnings.warn(
            f'Failed query ({str(resp.status_code)}) : {str(resp.json()["status"])} {str(resp.url)}'
        )
        return None

    def __get_tokens(self):
        params = {
            "username": self.username,
            "password": self._password,
        }
        sub_path = "token/"
        url = urljoin(self.api_root, sub_path)
        resp = requests.post(url, data=params)
        if resp.status_code == 401:
            raise Exception(f"Failed authentication {resp.text}")

        resp = resp.json()
        self.access_token = resp["access"]
        self.refresh_token = resp["refresh"]

    def __renew_access_token(self):
        """
        Will  renew the access token by sending a post request to server
        """
        params = {"refresh": self.refresh_token}
        sub_path = "token/refresh/"
        url = urljoin(self.api_root, sub_path)
        resp = requests.post(url, data=params)
        if resp.status_code == 200:
            resp = resp.json()
            self.access_token = resp["access"]

    def __token_verif_and_renew(self):
        """
        Will check if the token is valid and renew it if its needed
        """
        params = {"token": self.refresh_token}
        sub_path = "token/verify/"
        url = urljoin(self.api_root, sub_path)
        resp = requests.post(url, data=params)
        if resp.status_code == 401:
            self.__get_tokens()  # refresh all the tokens
        if resp.status_code == 200:
            self.__renew_access_token()  # refresh only access token


def _parse_timestamps(dt: datetime.datetime):
    """
    Return datetime.datetime objects as suitable strings for the API

    :param dt: timestamp
    :type dt: datetime.datetime
    """

    return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")
