"""
All views for everything related to the User
"""

import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest

from rest_framework import permissions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import DestroyAPIView

from services.file_conversion import in_memory_uploaded_file_to_bytes
from .tasks import update_profile
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from .services.auth import OperationForUserAuth


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
            "update": (permissions.IsAuthenticated,),
            "patrial_update": (permissions.IsAuthenticated,),
        }
        permissions_list = [
            permission() for permission in permission_classes.get(self.action, [])
        ]
        return permissions_list or super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        if user := cache.get("user"):
            logger.info("Пользователь найден в кэше")
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        user = self.get_object()
        cache.set("user", user, timeout=600)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args, **kwargs):
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
        user_data = User.objects.get(pk=user.id)
        cache.set("user", user_data, timeout=600)
        # Adding the required tokens to cookies
        OperationForUserAuth.set_cookies(user, response)
        logger.debug(request.COOKIES.get("access"))
        return response

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

    @staticmethod
    def task_launching(request):
        """
        Preparing and launching a task
        """
        instance = request.user
        avatar = request.FILES.get("avatar")
        file_to_byte = in_memory_uploaded_file_to_bytes(avatar)[0]
        request.data["avatar"] = {
            "byte": file_to_byte,
            "name": avatar.name,
            "content_type": "image/jpeg",
        }
        data = {
            "request": request.data,
            "instance": {
                "avatar": instance.avatar,
                "pk": instance.pk,
            },
        }
        update_profile.delay(data)


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
            user_data = User.objects.get(pk=user.id)
            cache.set("user", user_data, timeout=600)
            logger.debug(cache.get("user"))
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
