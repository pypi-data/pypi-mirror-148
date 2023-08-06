from requests import post
import logging


class api:
    def __init__(self, url, user, psw):
        self.url = url
        self.user = user
        self.psw = psw
        self.token = self.login()

    def zabbix_request(self, data):

        response = post(self.url, json=data)
        response = response.json()

        try:
            if 'result' in response.keys():
                return response['result']
            elif 'error' in response.keys():
                logging.error(f'Zabbix API Request retourned an error: '
                              f'{{'
                              f'code: {response["error"]["code"]}, '
                              f'message: {response["error"]["message"]}, '
                              f'data: {response["error"]["data"]}'
                              f' }}')
        except Exception as e:
            logging.error(e+response)

    def login(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.psw
            },
            "id": 1,
            "auth": None
        }
        response = self.zabbix_request(data)
        return response

    def request(self, method, params):
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": self.token,
            "id": 2
        }

        return self.zabbix_request(data)
