"""
All views for everything related to the Ad
"""

import logging

from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.parsers import MultiPartParser, JSONParser

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
