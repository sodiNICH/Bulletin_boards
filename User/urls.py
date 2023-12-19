"""
URL routing for everything related to the User
"""

from django.urls import include, path

from rest_framework import routers

from . import views
from .services import render_template


router = routers.DefaultRouter()
router.register(
    r"user",
    views.UserViewSet,
    basename="user",
)

urlpatterns = [
    path(
        "",
        render_template.UserProfileTemplate.as_view(),
        name="profile-template",
    ),
    path(
        "register/",
        render_template.UserRegisterTemplate.as_view(),
        name="register-template",
    ),
    path(
        "login/",
        render_template.UserLoginTemplate.as_view(),
        name="login-template",
    ),
    path(
        "api/",
        views.ProfileUserAPI.as_view(),
        name="profile-api",
    ),
    path(
        "login/api/",
        views.UserLoginAPI.as_view(),
        name="login-api",
    ),
    path(
        "logout/api/",
        views.UserLogoutAPI.as_view(),
        name="logout-api",
    ),
    path(
        'register/validated/',
        views.ValidatedDataAPI.as_view(),
        name="validated-register",
    ),
    path(
        "",
        include(router.urls),
    ),
]
