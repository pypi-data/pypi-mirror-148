import requests
from datomizer.utils import constants

CLIENT = "direct-sdk"


def get_domain_by_username(username: str, env: str = 'app') -> str:
    response = requests.get(constants.ONBOARDING_GET_USER_DOMAIN_DEFAULT % (env, username))
    return response.url.replace("https://", "").split('/')[0]


def get_realm_by_domain(domain: str) -> str:
    response = requests.get(constants.IDENTITY_GET_REALM_BY_DOMAIN % domain)
    return response.text


def post_token(realm: str, domain: str, username: str, password: str):
    client_props = {
        "client_id": CLIENT,
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(constants.KEYCLOAK_GET_TOKEN_URL % (domain, realm), client_props)
    return response.json()


def post_refresh_token(realm: str, domain: str, token: str):
    client_props = {
        "client_id": CLIENT,
        "grant_type": "refresh_token",
        "refresh_token": token
    }

    response = requests.post(constants.KEYCLOAK_GET_TOKEN_URL % (domain, realm), client_props)
    return response.json()


def post_log_out(realm: str, domain: str, token: str, refresh_token: str):
    headers = {"Authorization": f"Bearer {token}"}
    client_props = {
        "client_id": CLIENT,
        "refresh_token": refresh_token
    }
    response = requests.post(constants.KEYCLOAK_LOGOUT_URL % (domain, realm), client_props, headers=headers)
    return response.text
