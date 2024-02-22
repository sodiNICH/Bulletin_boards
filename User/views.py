"""
All views for everything related to the User
"""

import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AbstractBaseUser

from django.http import HttpRequest

from rest_framework import permissions, status, mixins, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import DestroyAPIView
from advertisements.models import Advertisements

from services.file_conversion import in_memory_uploaded_file_to_bytes
from .tasks import update_profile
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from .services.auth import OperationForUserAuth
from .services.favorite_manager import (
    searching_ad,
    addind_to_favorite,
    deleting_to_favorite,
    user_favorites_and_response,
)
from .services.subscriptions_manager import (
    get_to_subscriptions,
    searchig_seller,
    addind_to_subscriptions,
    deleting_to_subscriptions,
)


User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    mixins = (mixins.UpdateModelMixin,)
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    def get_permissions(self):
        permission_classes = {
            "retrieve": (permissions.AllowAny,),
            "list": (permissions.IsAdminUser,),
            "create": (permissions.AllowAny,),
        }
        permissions_list = [
            permission() for permission in permission_classes.get(self.action, [])
        ]
        return permissions_list or super().get_permissions()

    def create(self, request, *args, **kwargs):
        # Creating new user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(
            serializer.validated_data,
        )
        # Creating http response
        response = Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": "Data valid",
                "id": user.id,
            },
        )

        # Adding user data in cache
        user_data: AbstractBaseUser = User.objects.get(pk=user.id)
        cache.set(f"user_{user.id}", user_data, timeout=600)
        # Adding the required tokens to cookies
        OperationForUserAuth.set_cookies(user, response)
        logger.debug(request.COOKIES.get("access"))
        return response

    def retrieve(self, request, *args, **kwargs) -> Response:
        return self.caching_user(kwargs["pk"], request) or super().retrieve(
            request, *args, **kwargs
        )

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        self.task_launching(request)
        response = Response(
            data={
                "message": "User data updated successfully",
            },
            status=status.HTTP_200_OK,
        )
        logger.debug("Response отправлен")
        return response

    def caching_user(self, pk, request) -> Response | None:
        """
        Checking user for caching
        """
        user_cache_key = f"user_{pk}"

        if cached_user := cache.get(user_cache_key):
            serializer = self.get_serializer(cached_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        cached_user: AbstractBaseUser = User.objects.get(pk=pk)
        timeout = 600 if request.user.id == pk else 300
        cache.set(user_cache_key, cached_user, timeout=timeout)
        return None

    @staticmethod
    def task_launching(request) -> None:
        """
        Preparing and launching a task
        """
        if avatar := request.FILES.get("avatar"):
            file_to_byte: tuple[bytes, str] = in_memory_uploaded_file_to_bytes(avatar)
            request.data["avatar"] = {
                "byte": file_to_byte[0],
                "name": file_to_byte[1],
                "content_type": "image/jpeg",
            }
        update_profile.delay(request.data, user_id=request.user.id)


class UserLoginAPI(ObtainAuthToken):
    """
    Endpoint for Auth
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Handle user login
        """
        # Create serializer class
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        # Data validation
        if user := serializer.validated_data.get("user"):
            logger.debug(user)
            response = Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "Authorization was successful",
                    "id": user.id,
                },
            )
            # Adding user data in cache
            user_data: AbstractBaseUser = User.objects.get(pk=user.id)
            cache.set(f"user_{user.id}", user_data, timeout=600)
            logger.debug(cache.get(f"user_{user.id}"))
            # Adding the required tokens to cookies
            OperationForUserAuth.set_cookies(user, response)
            logger.debug("Token created")
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class UserLogoutAPI(DestroyAPIView):
    """
    Endpoint for Logout
    """

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request: HttpRequest, *args, **kwargs):
        """
        Handle user logout
        """
        logger.debug(request.user)
        response = Response(
            status=status.HTTP_204_NO_CONTENT,
            data="Account logout executed",
        )
        cache.delete("user")
        OperationForUserAuth.delete_cookie(response)
        return response


class FavoriteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_and_ad: tuple[User, Advertisements] = searching_ad(request)
        return addind_to_favorite(*user_and_ad)

    def delete(self, request, *args, **kwargs):
        user_and_ad: tuple[User, Advertisements] = searching_ad(request)
        return deleting_to_favorite(*user_and_ad)

    def get(self, request, *args, **kwargs):
        return user_favorites_and_response(request)


class SubscriptionsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_seller: tuple[User, User] = searchig_seller(request)
        return addind_to_subscriptions(*user_seller)

    def delete(self, request, *args, **kwargs):
        user_seller: tuple[User, User] = searchig_seller(request)
        return deleting_to_subscriptions(*user_seller)

    def get(self, request, *args, **kwargs):
        return get_to_subscriptions(request)
