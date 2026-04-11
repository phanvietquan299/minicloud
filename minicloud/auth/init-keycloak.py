import json
import time
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "http://authentication-identity-server:8080/auth"
REALM = "realm_sv001"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"


def request_json(url, method="GET", token=None, body=None):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read().decode("utf-8")
        if content:
            return json.loads(content)
        return None


def request_form(url, data):
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_keycloak():
    token_url = f"{BASE_URL}/realms/master/protocol/openid-connect/token"
    for _ in range(60):
        try:
            return request_form(
                token_url,
                {
                    "grant_type": "password",
                    "client_id": "admin-cli",
                    "username": ADMIN_USERNAME,
                    "password": ADMIN_PASSWORD,
                },
            )["access_token"]
        except Exception:
            time.sleep(2)
    raise RuntimeError("Keycloak did not become ready in time")


def ensure_user(token, username, password):
    users_url = f"{BASE_URL}/admin/realms/{REALM}/users"
    existing = request_json(f"{users_url}?username={urllib.parse.quote(username)}", token=token)
    if existing:
        user_id = existing[0]["id"]
    else:
        request_json(
            users_url,
            method="POST",
            token=token,
            body={
                "username": username,
                "enabled": True,
                "emailVerified": True,
                "requiredActions": [],
            },
        )
        existing = request_json(f"{users_url}?username={urllib.parse.quote(username)}", token=token)
        user_id = existing[0]["id"]

    request_json(
        f"{users_url}/{user_id}",
        method="PUT",
        token=token,
        body={
            "id": user_id,
            "username": username,
            "enabled": True,
            "emailVerified": True,
            "requiredActions": [],
        },
    )
    request_json(
        f"{users_url}/{user_id}/reset-password",
        method="PUT",
        token=token,
        body={"type": "password", "value": password, "temporary": False},
    )


def main():
    token = wait_for_keycloak()
    ensure_user(token, "sv01", "sv01")
    ensure_user(token, "sv02", "sv02")
    print("Keycloak users initialized")


if __name__ == "__main__":
    main()