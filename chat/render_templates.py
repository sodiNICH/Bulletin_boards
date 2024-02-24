from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect


class ListChatsTemplate(APIView):
    """
    Register template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("register-template"))
        path_template = "chat/list_chats.html/"
        return Response(template_name=path_template)


class DetailChatTemplate(APIView):
    """
    Register template renderer
    """

    def get(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("register-template"))
        path_template = "chat/detail_chat.html/"
        return Response(template_name=path_template)
