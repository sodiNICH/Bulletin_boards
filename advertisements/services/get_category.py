from rest_framework import status
from rest_framework.response import Response

from advertisements.models import Advertisements
from advertisements.serializers import AdSerializer


def list_ad_category_and_response(field, request, **kwargs):
    data = kwargs.get(field)
    if data:
        ads = Advertisements.objects.filter(**{field + "__iexact": data})
        serializer_ads = AdSerializer(ads, many=True, context={"request": request})
        return Response(data=serializer_ads.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)