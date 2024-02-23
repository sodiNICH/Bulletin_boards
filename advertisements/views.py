"""
All views for everything related to the Ad
"""

import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest
from django.db.models import Q

from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser

from services.file_conversion import in_memory_uploaded_file_to_bytes
from .tasks import create_ad_task
from .services.get_category import list_ad_category_and_response
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

    def destroy(self, request, *args, **kwargs):
        ad_id: int | None = kwargs.get("id")
        ad: Advertisements | Http404 = get_object_or_404(Advertisements, pk=ad_id)

        if ad in request.user.advertisements.all():
            return super().destroy(request, *args, **kwargs)
        return Response(
            data={"message": "You can't delete someone else's ad!"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def retrieve(self, request, *args, **kwargs):
        ad: Advertisements = get_object_or_404(self.queryset, pk=kwargs["pk"])
        similar_ads = Advertisements.objects.filter(
            Q(category=ad.category)
            | Q(subcategory=ad.subcategory)
            | Q(title__icontains=ad.title)
        ).exclude(id=ad.id)[:5]

        logger.debug(similar_ads)
        serializer = self.get_serializer(ad, context={"request": request})
        similar_ads_serializer = self.get_serializer(
            similar_ads, many=True, context={"request": request}
        )

        serializer_data = serializer.data
        serializer_data["similar_ads"] = similar_ads_serializer.data
        return Response(
            status=status.HTTP_200_OK,
            data=serializer_data,
        )

    @staticmethod
    def task_launching(request) -> None:
        """
        Preparing and launching a task
        """
        images = request.FILES.getlist("images")
        images_bytes = list(map(in_memory_uploaded_file_to_bytes, images))
        request.data["images"] = images_bytes
        request.data["owner"] = request.user.id
        create_ad_task.delay(request.data)


class ListADCategory(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        return list_ad_category_and_response("category", request, *args, **kwargs)


class ListADSubcategory(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        return list_ad_category_and_response("subcategory", request, *args, **kwargs)
