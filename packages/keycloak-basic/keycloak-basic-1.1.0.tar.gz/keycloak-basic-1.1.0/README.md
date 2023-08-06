# Keycloak-Basic

All the libraries I found for Keycloak are outdated and not _nearly_ generic enough, so here's a new one.

## Documentation

**Installing**

```bash
python -m pip install keycloak-basic
```

**Usage**

```python
from keycloak import Keycloak, AccessToken, UserInfo

keycloak: Keycloak = Keycloak(
    "http(s)://<host>:<port>", # Keycloak server URL with no trailing path
    "<realm name>", # Name of realm to authenticate in
    "<client id>", # Client ID
    client_secret = "<client secret" # Client secret, if present
)

token: AccessToken = keycloak.login(
    "<username>", # User username
    "<password>" # User password
) -> AccessToken

keycloak.authenticated # Boolean, true if logged in
keycloak.isScoped("scope") -> bool # True if current token has scope

info: UserInfo = keycloak.userinfo() -> UserInfo object

keycloak.refresh() -> AccessToken # Refreshes connection
keycloak.logout() # Logs out
```
