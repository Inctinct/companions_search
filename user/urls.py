from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from user.views import CallbackView, LoginView, HomeView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("callback", CallbackView.as_view(), name="callback"),
    path(
        "logout",
        LogoutView.as_view(
            next_page=(getattr(settings, "LOGOUT_REDIRECT_URL", "/") or "/"),
        ),
        name="logout",
    ),
    path("", HomeView.as_view()),
    re_path(r"^token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    re_path(r"^token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
