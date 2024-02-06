"""
All views for everything related to the Ad
"""

import logging

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.core.cache import cache

from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser

from services.file_conversion import in_memory_uploaded_file_to_bytes
from .tasks import create_ad_task
from .models import Advertisements
from .serializers import AdSerializer


User = get_user_model()
logger = logging.getLogger(__name__)


class AdViewSet(viewsets.ModelViewSet):
    """
    Viewset for Ad
    """

    queryset = Advertisements.objects.all()
    serializer_class = AdSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    mixins = (mixins.UpdateModelMixin,)
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    def create(self, request: HttpRequest, *args, **kwargs):
        self.task_launching(request)
        return Response(
            data={
                "message": "Ad published",
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def task_launching(request):
        """
        Preparing and launching a task
        """
        images = request.FILES.getlist("images")
        images_bytes = list(map(in_memory_uploaded_file_to_bytes, images))
        request.data["images"] = images_bytes
        request.data["owner"] = request.user.id
        create_ad_task.delay(request.data)
