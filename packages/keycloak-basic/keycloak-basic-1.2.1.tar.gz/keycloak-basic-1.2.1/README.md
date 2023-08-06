# Keycloak-Basic

All the libraries I found for Keycloak are outdated and not _nearly_ generic enough, so here's a new one.

## Documentation

**Installing**

```bash
python -m pip install keycloak-basic
```

**Usage**

```python
from keycloak import Keycloak, Token, UserInfo

keycloak: Keycloak = Keycloak(
    "http(s)://<host>:<port>", # Keycloak server URL with no trailing path
    "<realm name>", # Name of realm to authenticate in
    "<client id>", # Client ID
    client_secret = "<client secret" # Client secret, if present
)

token: Token = keycloak.auth(
    "<username>", # User username
    "<password>" # User password
) -> Token

token.authenticated # Boolean, true if logged in
token.isScoped("scope") -> bool # True if current token has scope

info: UserInfo = token.info() -> UserInfo object

token.refresh() # Refreshes connection
token.logout() # Logs out

keycloak.load_token(token.content) -> Token # Loads token from dict
```
