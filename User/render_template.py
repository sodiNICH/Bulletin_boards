"""
Service for rendering HTML-templates
"""

import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.urls import reverse
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class BaseTemplateView(APIView):
    permission_classes = (AllowAny,)

    def get_template(self):
        raise NotImplementedError("Subclasses must implement get_template method.")

    def get(self, request, *args, **kwargs):
        path_template = self.get_template()
        return Response(template_name=path_template)


class UserRegisterTemplate(BaseTemplateView):
    """
    Register template renderer
    """

    def get_template(self):
        return "User/register.html/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("profile-template", kwargs={"pk": request.user.id}))
        return super().get(request, *args, **kwargs)


class UserLoginTemplate(UserRegisterTemplate):
    """
    Login template renderer
    """

    def get_template(self):
        return "User/login.html/"


class UserProfileEditTemplate(BaseTemplateView):
    """
    User profile edit template renderer
    """

    permission_classes = (IsAuthenticated,)

    def get_template(self):
        return "User/edit_profile.html/"


class UserProfileTemplate(BaseTemplateView):
    def get_template(self):
        if self.kwargs.get("pk") == self.request.user.id:
            return "User/auth_profile.html/"
        else:
            return "User/profile.html/"


class UserFavoriteTemplate(BaseTemplateView):
    """
    Favorites list advert template
    """
    permission_classes = (IsAuthenticated,)

    def get_template(self):
        return "User/favorites_list.html"


class UserSubscriptionsTemplate(BaseTemplateView):
    def get_template(self):
        return "User/subscriptions_list.html"
