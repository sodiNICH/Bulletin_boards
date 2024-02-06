from django.urls import path, include

from rest_framework import routers

from . import views
from . import render_template


router = routers.DefaultRouter()
router.register(
    r"ad/api",
    views.AdViewSet,
    basename="ad-api",
)


urlpatterns = [
    # Template endpoints
    path(
        "create/ad/",
        render_template.CreateAdTemplate.as_view(),
        name="template-create-ad",
    ),
    path(
        "ad/<int:pk>/",
        render_template.DetailAdTemplate.as_view(),
        name="template-detail-ad",
    ),
    path("", render_template.MainPageTemplate.as_view(), name="template-mainpage"),
    # API endpoints
    path(
        "",
        include(router.urls),
    ),
]
