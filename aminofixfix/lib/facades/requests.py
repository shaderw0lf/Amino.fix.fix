from __future__ import annotations
# ^ this thing should fix problem for python3.9 and lower(?)

from requests import Session, Response


class RequestsClient:
    """
    Facade for Requests library to be compactable with HTTPX client style.
    Also made for escaping 429.

    [TODO]: timeouts
    """

    def __init__(self, headers: dict, base_url: str, proxies: dict = {}, **kwargs):
        """
        Init of Requests Client.
        """
        self.__client: Session = Session()
        self.__base_url = base_url
        self.__proxies = proxies
        self.__main_headers = headers

    def request(
        self,
        method: str,
        path: str,
        headers: dict = {},
        data: str | bytes | dict | None = None,
    ) -> Response:
        """
        Request.

        Args:
        - method: str (GET, POST, DELETE, PUT)
        - url: str
        - headers: dict = {}
        - etc. just for not breaking stuff

        Returns:
        - object `requests.Response`
        """
        while True:
            r = self.__client.request(
                method=method,
                url=self.__base_url + path,
                headers=self.__main_headers | headers,
                proxies=self.__proxies,
                data=data,
            )
            if r.status_code != 429:
                return r

    def get(self, path: str, headers: dict = {}, **kwargs) -> Response:
        """
        Get request.

        Args:
        - path: str
        - headers: dict = {}
        - etc. just for not breaking stuff

        Returns:
        - object `requests.Response`
        """
        return self.request("GET", path, headers)

    def post(
        self,
        path: str,
        headers: dict = {},
        data: str | dict | bytes | None = None,
        **kwargs,
    ) -> Response:
        """
        Post request.

        Args:
        - path: str
        - headers: dict = {}
        - data: str | dict | bytes | None = None (it will autodetect if its dict and send it as json but not just data)
        - etc. just for not breaking stuff

        Returns:
        - object `requests.Response`
        """
        return self.request("POST", path, headers, data)

    def delete(
        self,
        path: str,
        headers: dict = {},
        data: str | dict | bytes | None = None,
        **kwargs,
    ) -> Response:
        """
        Delete request.

        Args:
        - path: str
        - headers: dict = {}
        - data: str | dict | bytes | None = None (it will autodetect if its dict and send it as json but not just data)
        - etc. just for not breaking stuff

        Returns:
        - object `requests.Response`
        """
        return self.request("DELETE", path, headers, data)
