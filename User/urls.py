"""
URL routing for everything related to the User
"""

from django.urls import include, path

from rest_framework import routers

from . import views
from .services import render_template


router = routers.DefaultRouter()
router.register(
    r"user/api",
    views.UserViewSet,
    basename="user-api",
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
        "edit/",
        render_template.UserProfileEditTemplate.as_view(),
        name="profile-edit",
    ),
    # path(
    #     "user/main/api/",
    #     views.ProfileUserAPI.as_view({"get": "retrieve", "patch": "update"}),
    #     name="profile-api",
    # ),
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
        "register/validated/",
        views.ValidatedDataAPI.as_view(),
        name="validated-register",
    ),
    path(
        "",
        include(router.urls),
    ),
]
