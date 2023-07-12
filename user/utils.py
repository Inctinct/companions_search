import requests
from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from project.settings import (
    GITHUB_OAUTH_SCOPES,
    GITHUB_OAUTH_CLIENT_ID,
    GITHUB_OAUTH_CALLBACK_URL,
    GITHUB_OAUTH_SECRET,
)


def get_github_user_data(token):
    headers = {"Authorization": "token %s" % token}
    r = requests.get("https://api.github.com/user", headers=headers)
    r.raise_for_status()
    return r.json()


def get_user(token):
    data = get_github_user_data(token)
    user_model = get_user_model()
    user, _ = user_model.objects.update_or_create(
        {user_model.USERNAME_FIELD: data["login"]}, **dict(id=data["id"])
    )
    return user


def get_redirect_uri():
    scopes = GITHUB_OAUTH_SCOPES
    return "https://github.com/login/oauth/authorize?%s" % urlencode(
        {
            "client_id": GITHUB_OAUTH_CLIENT_ID,
            "redirect_uri": GITHUB_OAUTH_CALLBACK_URL,
            "scope": " ".join(set(scopes if scopes else [])),
            "response_type": "code",
        }
    )


def get_github_token(session_code):
    data = {
        "code": session_code,
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "client_secret": GITHUB_OAUTH_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": GITHUB_OAUTH_CALLBACK_URL,
    }
    return data
