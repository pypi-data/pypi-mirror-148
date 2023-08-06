from .dataclass import Dataclass
import requests
import time
from .user import UserInfo
from .util import *

class Token(Dataclass):
    EXCLUDE = ["content", "keycloak"]
    def __init__(self, content: dict, keycloak) -> None:
        super().__init__(content)
        self.keycloak = keycloak
        self.last_auth = time.time()
        self.authenticated = True

    @property
    def token(self) -> str:
        return self.content["access_token"]
    
    @property
    def expires(self) -> str:
        return self.content["expires_in"]

    @property
    def refresh_expires(self) -> str:
        return self.content["refresh_expires_in"]
    
    @property
    def token_refresh(self) -> str:
        return self.content["refresh_token"]

    @property
    def token_type(self) -> str:
        return self.content["token_type"]
    
    @property
    def not_before_policy(self) -> int:
        return self.content["not-before-policy"]
    
    @property
    def session_state(self) -> str:
        return self.content["session_state"]
    
    @property
    def scope(self) -> list[str]:
        return self.content["scope"].split(" ")
    
    @property
    def is_expired(self) -> bool:
        return time.time() > self.last_auth + self.expires
    
    @property
    def is_refresh_expired(self) -> bool:
        return time.time() > self.last_auth + self.refresh_expires
    
    def check_auth(self):
        if not self.authenticated:
            return False
        
        if self.is_expired and not self.is_refresh_expired:
            self.refresh()
            return True
        elif not self.is_expired:
            return True
        else:
            self.authenticated = False
            return False
    
    def make_auth_header(self) -> str:
        """Makes auth header

        Returns:
            str: <token type> <token> (Example: "Bearer 12345asdfg")
        """
        return self.token_type + " " +self.token
    
    def info(self):
        """Get User Info of user

        Raises:
            KeycloakError: Raised if not logged in
            KeycloakConnectionError: Raised if an unspecified server error occurs

        Returns:
            UserInfo: User Info object
        """
        if not self.check_auth():
            raise KeycloakError("Not authenticated. This token is dead. Login again.")
        resp = requests.get(self.keycloak.endpoint_userinfo, headers={
            "Authorization": self.make_auth_header()
        })
        if resp.status_code >= 400:
            raise KeycloakConnectionError(resp.status_code, resp.text)
        
        return UserInfo(resp.json())
    
    def logout(self) -> None:
        """Logs out from keycloak

        Raises:
            KeycloakError: Raised if not logged in
            KeycloakConnectionError: Raised if an unexpected error occurs
        """
        if not self.check_auth():
            raise KeycloakError("Not authenticated. This token is dead. Login again.")
        
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": self.make_auth_header()
        }
        if self.keycloak.client_secret:
            resp = requests.post(self.keycloak.endpoint_logout, data=formencode({
                "client_id": self.keycloak.client_id,
                "client_secret": self.keycloak.client_secret,
                "refresh_token":self.token_refresh
            }), headers=headers)
        else:
            resp = requests.post(self.keycloak.endpoint_logout, data=formencode({
                "client_id": self.keycloak.client_id,
                "refresh_token":self.token_refresh
            }), headers=headers)
        
        if resp.status_code >= 400:
            raise KeycloakConnectionError(resp.status_code, resp.text)
        
        self.authenticated = False
    
    def refresh(self):
        """Refreshes token

        Raises:
            KeycloakError: Raised if not logged in
            KeycloakConnectionError: Raised if an unexpected connection error occurs
        """
        if self.is_refresh_expired or not self.authenticated:
            raise KeycloakError("Not authenticated. This token is dead. Login again.")
        
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        if self.keycloak.client_secret:
            resp = requests.post(self.keycloak.endpoint_token, data=formencode({
                "client_id": self.keycloak.client_id,
                "client_secret": self.keycloak.client_secret,
                "refresh_token":self.token_refresh,
                "grant_type": "refresh_token",
                "scope": "openid profile"
            }), headers=headers)
        else:
            resp = requests.post(self.keycloak.endpoint_token, data=formencode({
                "client_id": self.keycloak.client_id,
                "refresh_token":self.token_refresh,
                "grant_type": "refresh_token",
                "scope": "openid profile"
            }), headers=headers)
        
        if resp.status_code >= 400:
            raise KeycloakConnectionError(resp.status_code, resp.text)
        
        self.content = resp.json()
        self.authenticated = True
        self.last_auth = time.time()
    
    def is_scoped(self, scope: str) -> bool:
        """Checks if scope exists in token

        Args:
            scope (str): Scope to check

        Raises:
            KeycloakError: Raised if token is dead

        Returns:
            bool: True if token is in scope
        """
        if not self.check_auth():
            raise KeycloakError("Not authenticated. This token is dead. Login again.")
        
        return scope in self.scope