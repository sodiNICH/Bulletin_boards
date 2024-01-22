"""
Service for rendering HTML-templates
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect


class CreateAdTemplate(APIView):
    """
    Register template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("profile-template", kwargs={"pk": request.user.id}))
        path_template = "advertisements/create_ad.html/"
        return Response(template_name=path_template)
