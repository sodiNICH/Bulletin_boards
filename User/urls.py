"""
URL routing for everything related to the User
"""

from django.urls import include, path

from rest_framework import routers

from . import views
from .validators import ValidatedDataAPI
from . import render_template


router = routers.DefaultRouter()
router.register(
    r"api/v1/user",
    views.UserViewSet,
    basename="user-api",
)

urlpatterns = [
    # Template endpoints
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
    path(
        "<int:pk>/",
        render_template.UserProfileTemplate.as_view(),
        name="profile-template",
    ),
    path(
        "favorites/",
        render_template.UserFavoriteTemplate.as_view(),
        name="favorite-template",
    ),
    path(
        "subscriptions/",
        render_template.UserSubscriptionsTemplate.as_view(),
        name="subscriptions-template",
    ),
    # API endpoints
    path(
        "",
        include(router.urls),
    ),
    path(
        "api/v1/favorites/",
        views.FavoriteAPIView.as_view(),
        name="favorites-manager",
    ),
    path(
        "api/v1/subscriptions/",
        views.SubscriptionsAPIView.as_view(),
        name="subscriptions-manager",
    ),
    path(
        "api/v1/login/",
        views.UserLoginAPI.as_view(),
        name="login-api",
    ),
    path(
        "api/v1/logout/",
        views.UserLogoutAPI.as_view(),
        name="logout-api",
    ),
    # Endpoint for validating data
    path(
        "api/v1/register/validated/",
        ValidatedDataAPI.as_view(),
        name="validated-register",
    ),
]
