"""
Service for rendering HTML-templates
"""

import logging

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class UserRegisterTemplate(APIView):
    """
    Register template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("profile-template", kwargs={"pk": request.user.id}))
        path_template = "User/register.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserLoginTemplate(APIView):
    """
    Login template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("profile-template", kwargs={"pk": request.user.id}))
        path_template = "User/login.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserProfileEditTemplate(APIView):
    """
    User profile edit template renderer
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest, *args, **kwargs):
        logger.debug(request.user.username)
        path_template = "User/edit_profile.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserProfileTemplate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest, *args, **kwargs):
        print(kwargs.get("pk") == request.user.id)
        if kwargs.get("pk") == request.user.id:
            path_template = "User/auth_profile.html/"
        else:
            path_template = "User/profile.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserFavoriteTemplate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            path_template = "User/favorites_list.html"
            return Response(template_name=path_template)
        return redirect(reverse("register-template"))


@renderer_classes([TemplateHTMLRenderer])
class UserSubscriptionsTemplate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            path_template = "User/subscriptions_list.html"
            return Response(template_name=path_template)
        return redirect(reverse("register-template"))
