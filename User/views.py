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

from rest_framework import permissions, status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from .services.auth import AuthUser
from .validators import ValidatorsObjectRegister


User = get_user_model()
Auth_obj = AuthUser()
Valid_register = ValidatorsObjectRegister()
logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    """
    Viewset for user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_permissions(self):
        permission_classes = {
            "retrieve": (permissions.IsAuthenticated,),
            "list": (permissions.IsAdminUser,),
            "create": (permissions.AllowAny,),
        }
        permissions_list = [
            permission() for permission in permission_classes.get(self.action, [])
        ]
        return permissions_list or super().get_permissions()

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(
            serializer.validated_data,
        )
        response = Response(
            status=status.HTTP_201_CREATED,
        )

        Auth_obj.set_cookies(user, response)
        logger.debug(request.COOKIES.get("access"))
        return response


class ProfileUserAPI(generics.RetrieveAPIView):
    """
    Handle user data
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer  # Замените на ваш сериализатор

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
