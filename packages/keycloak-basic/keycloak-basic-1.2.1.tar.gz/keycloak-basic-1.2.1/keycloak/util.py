from urllib.parse import quote

class KeycloakError(Exception):
    pass

class KeycloakConnectionError(KeycloakError):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(f"Request to keycloak failed with code {code}: {message}")

def formencode(data: dict):
    return "&".join([quote(k) + "=" + quote(v) for k, v in data.items()])