from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import mixins, permissions

from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    mixins = (mixins.UpdateModelMixin,)
    parser_classes = (
        JSONParser,
        MultiPartParser,
    )
