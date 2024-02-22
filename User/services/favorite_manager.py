from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status

from advertisements.models import Advertisements
from advertisements.serializers import AdSerializer


User = get_user_model()


def searching_ad(request) -> tuple[User, Advertisements]:
    user = request.user
    ad_id = request.data.get("ad")
    ad = get_object_or_404(Advertisements, pk=ad_id)
    return user, ad


def addind_to_favorite(user: User, ad: Advertisements) -> Response:
    if ad not in user.favorites.all():
        user.favorites.add(ad)
    return Response(status=status.HTTP_201_CREATED, data={"message": "Favorites added"})


def deleting_to_favorite(user: User, ad: Advertisements) -> Response:
    if ad in user.favorites.all():
        user.favorites.remove(ad)
    return Response(
        status=status.HTTP_204_NO_CONTENT,
        data={"message": "Favorites removed"},
    )


def user_favorites_and_response(request: HttpRequest) -> Response:
    user = request.user
    favorites = user.favorites.all()
    serializer = AdSerializer(favorites, many=True, context={"request": request})
    response = Response(
        status=status.HTTP_200_OK,
        data=serializer.data,
    )
    return response
