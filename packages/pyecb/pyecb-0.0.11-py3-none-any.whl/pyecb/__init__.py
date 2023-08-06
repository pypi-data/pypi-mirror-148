# -*- coding: utf-8 -*-
__version__ = '0.1.0'


import requests


class ECB:

    def __init__(
            self,
            api_key=None):
        """
        ECB

        Create a new instance of the ECB API

        Args:
            api_key (str): The API Key for authentication

        """
        self.api_key = api_key
        self.base_url = " https://www.play-cricket.com/api/v2/"

    def _get_api_content(self,
                         api_name=None,
                         **kwargs):
        """
        _get_api_content

        Return the content from the API as a dict

        Args:
            api_name (str): The Name of the API (clubs, team, etc)
            **kwargs: Further arguments to be passed as a parameter
        """
        url = self.base_url + "/" + api_name + ".json"
        params = {"api_token": self.api_key}
        for k, v in kwargs.items():
            params.update({k: v})
        req = requests.get(url, params=params)
        status = req.status_code
        if status == 200:
            data = req.json()
        else:
            data = {}

        return {"status": status, "data": data}

    def get_club_data(self, club_id=None):
        data = self._get_api_content("clubs")
        return data
