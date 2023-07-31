from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import requests

from apps.user.tokens import get_tokens_for_user
from apps.user.utils import get_redirect_uri, get_github_token, get_user


class LoginView(APIView):
    def get(self, request):
        return HttpResponseRedirect(redirect_to=get_redirect_uri())


class CallbackView(APIView):
    def get(self, request):
        r = requests.post(
            "https://github.com/login/oauth/access_token",
            data=get_github_token(request.GET.get("code")),
        )
        r.raise_for_status()
        for s in filter(lambda s: "access_token" in s, r.text.split("&")):
            github_token = s.split("=")[1]
        login(
            self.request,
            get_user(github_token),
            **{"backend": settings.GITHUB_AUTHENTICATION_BACKENDS}
        )
        tokens = get_tokens_for_user(User.objects.get(username=get_user(github_token)))
        return Response(tokens, status=200)


class HomeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(status=200)
