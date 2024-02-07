from django.db.models import QuerySet
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework import status

from advertisements.models import Advertisements
from advertisements.serializers import AdSerializer


def adding_or_deleting_to_favorites(user: QuerySet, ad_id: int) -> Response:
    try:
        ad = Advertisements.objects.get(id=ad_id)
        if ad in user.favorites.all():
            user.favorites.remove(ad)
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={"message": "Favorites removed"},
            )
        user.favorites.add(ad)
        return Response(
            status=status.HTTP_201_CREATED, data={"message": "Favorites added"}
        )
    except Advertisements.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"message": "Advertisement not found"},
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
