from bodosdk.api.auth import AuthApi
from bodosdk.api.request_wrapper import RequestWrapper


class BackendApi:

    def __init__(self, auth_api: AuthApi, api_url="https://api.bodo.ai/api", requests=RequestWrapper()):
        self._requests = requests
        self._auth_api = auth_api
        self._base_url = api_url

    def get_auth_header(self):
        token = self._auth_api.auth_token
        return {
            'Authorization': f'Bearer {token}',
        }