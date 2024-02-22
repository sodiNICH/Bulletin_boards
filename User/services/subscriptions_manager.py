from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response

from User.serializers import UserSerializer


User = get_user_model()


def searchig_seller(request) -> tuple[User, User]:
    user = request.user
    seller_id = request.data.get("seller_id")
    seller = get_object_or_404(User, pk=seller_id)
    return user, seller


def addind_to_subscriptions(user: User, seller: User) -> Response:
    if user == seller:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": "You can't sign up for yourself"},
        )
    if seller not in user.subscriptions.all():
        user.subscriptions.add(seller)
        seller.subscribers.add(user)
    return Response(
        status=status.HTTP_201_CREATED,
        data={"message": f"Subscribe to {seller.username} subscribed"},
    )


def deleting_to_subscriptions(user: User, seller: User) -> Response:
    if user == seller:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": "You can't unsubscribe from yourself"},
        )
    if seller in user.subscriptions.all():
        user.subscriptions.remove(seller)
        seller.subscribers.remove(user)
    return Response(
        status=status.HTTP_204_NO_CONTENT,
        data={"message": f"Subscribe to {seller.username} disabled"},
    )


def get_to_subscriptions(request) -> Response:
    user = request.user
    subscriptions = user.subscriptions.all()
    serializer = UserSerializer(subscriptions, many=True, context={"request": request})
    response = Response(
        status=status.HTTP_200_OK,
        data=serializer.data,
    )
    return response
