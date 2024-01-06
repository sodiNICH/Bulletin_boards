"""
Service for rendering HTML-templates
"""

import logging

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated

from django.http import HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class UserRegisterTemplate(APIView):
    """
    Register template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("profile-template"))
        path_template = "User/register.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserLoginTemplate(APIView):
    """
    Login template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("profile-template"))
        path_template = "User/login.html/"
        return Response(template_name=path_template)


@renderer_classes([TemplateHTMLRenderer])
class UserProfileTemplate(APIView):
    """
    User profile template renderer
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest, *args, **kwargs):
        logger.debug(request.user.username)
        path_template = "User/profile.html/"
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