from django.urls import path, include

from rest_framework import routers

from . import views
from .services import render_template


router = routers.DefaultRouter()
router.register(
    r"ad/api",
    views.AdViewSet,
    basename="ad-api",
)


urlpatterns = [
    # Template endpoints
    path(
        "create/ad/", render_template.CreateAdTemplate.as_view(), name="template-create-ad",
    ),
    # API endpoints
    path(
        "",
        include(router.urls),
    ),
]
