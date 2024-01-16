"""
All views for everything related to the User
"""

import logging

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy

from rest_framework import permissions, status, mixins, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from .services.auth import AuthUser
from .services.edit_profile import EditProfile
from .validators import ValidatorsObjectRegister


User = get_user_model()
Auth_obj = AuthUser()
Valid_register = ValidatorsObjectRegister()
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
    parser_classes = (MultiPartParser, JSONParser, )

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        permission_classes = {
            "retrieve": (permissions.AllowAny,),
            "list": (permissions.IsAuthenticated,),
            "create": (permissions.AllowAny,),
            "update": (permissions.IsAuthenticated,),
            "patrial_update": (permissions.IsAuthenticated,),
        }
        permissions_list = [
            permission() for permission in permission_classes.get(self.action, [])
        ]
        return permissions_list or super().get_permissions()

    def list(self, request, *args, **kwargs):
        if self.get_object() == request.user:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args, **kwargs):
        logger.debug("проверка")
        logger.debug(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.debug("ошибка?")
        user = serializer.create(
            serializer.validated_data,
        )
        response = Response(
            status=status.HTTP_201_CREATED,
            data={"Данные валидны"}
        )

        Auth_obj.set_cookies(user, response)
        logger.debug(request.COOKIES.get("access"))
        return response

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        edit_object = EditProfile()
        return edit_object.update_and_response(request=request, instance=instance, serializer=serializer)


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
            )
            Auth_obj.set_cookies(user, response)
            logger.debug("Токен был создан")
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class UserLogoutAPI(APIView):
    """
    Endpoint for Logout
    """

    permission_classes = (permissions.IsAuthenticated,)

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.COOKIES.get("access"):
            raise Http404("Exit is impossible")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Handle user logout
        """
        logger.debug(request.user)
        response = redirect(
            reverse_lazy("register-template"),
        )
        Auth_obj.delete_cookie(response)
        return response


class ValidatedDataAPI(APIView):
    """
    View for validated data
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        return Valid_register.validate_field(request.POST)

    def handle_unknown_field(self):
        return Response(
            data={
                "error": "Unknown field",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
