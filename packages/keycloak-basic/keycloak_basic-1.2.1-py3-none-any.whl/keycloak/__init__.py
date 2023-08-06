import requests

from .token import Token
from .util import *


class Keycloak:
    def __init__(
        self,
        server_url: str,
        realm: str,
        client_id: str,
        client_secret: str = None,
        well_known: str = "/realms/{realm}/.well-known/openid-configuration",
    ):
        """Keycloak Constructor

        Args:
            server_url (str): URL of server [http(s)://host:port]
            realm (str): Name of Keycloak Realm
            client_id (str): Client ID to use
            client_secret (str, optional): Client secret, if present. Defaults to None.
            well_known (str, optional): Alternate URL to well_known page. Defaults to "/realms/sso/.well-known/openid-configuration".
        """

        # Set basic parameters
        self.server_url = server_url.rstrip("/") + "{path}"
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self._wellknown_url = well_known

        # Get Well-Known data
        resp = requests.get(self.server_url.format(path=well_known.format(realm=self.realm)))
        if resp.status_code >= 400:
            raise KeycloakConnectionError(resp.status_code, resp.text)
        
        self._wk_all = resp.json()

        self.endpoint_token = self._wk_all["token_endpoint"]
        self.endpoint_userinfo = self._wk_all["userinfo_endpoint"]
        self.endpoint_logout = self._wk_all["end_session_endpoint"]

        self.current_token: Token = None

    def auth(self, username: str, password: str) -> Token:
        """Logs user into Keycloak

        Args:
            username (str): Username
            password (str): Password

        Raises:
            KeycloakConnectionError: Raised on an unspecified connection error

        Returns:
            Token: Token
        """
        
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        if self.client_secret:
            resp = requests.post(self.endpoint_token, data=formencode({
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }), headers=headers)
        else:
            resp = requests.post(self.endpoint_token, data=formencode({
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": self.client_id,
            }), headers=headers)

        if resp.status_code >= 400:
            raise KeycloakConnectionError(resp.status_code, resp.text)
        return Token(resp.json(), self)
    
    def load_token(self, data: dict) -> Token:
        """Loads token from dict

        Args:
            data (dict): Access token

        Returns:
            Token: Token object
        """
        return Token(data, self)


