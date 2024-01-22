"""
All views for everything related to the User
"""

import logging

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest

from rest_framework import permissions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import DestroyAPIView

from config.minio_utils import MinIOFileManager
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from .services.auth import OperationForUserAuth
from .services.edit_profile import UserProfileEditor


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
        # Adding the required tokens to cookies
        OperationForUserAuth.set_cookies(user, response)
        logger.debug(request.COOKIES.get("access"))
        return response

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        edit_user_object = UserProfileEditor(MinIOFileManager, logger)
        return edit_user_object.update_profile_and_get_response(
            request=request, instance=instance, serializer=serializer
        )


class UserLoginAPI(ObtainAuthToken):
    """
    Endpoint for Auth
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Handle user login
        """
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        if user := serializer.validated_data.get("user"):
            logger.debug(user)
            response = Response(
                status=status.HTTP_200_OK,
                data={
                    "message": "Authorization was successful",
                    "id": user.id,
                },
            )
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
        OperationForUserAuth.delete_cookie(response)
        return response
