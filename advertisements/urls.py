from django.urls import path, include
from django.shortcuts import render

from rest_framework import routers

from . import views
from . import render_template


router = routers.DefaultRouter()
router.register(
    r"api/v1/advert",
    views.AdViewSet,
    basename="ad-api",
)


urlpatterns = [
    # Template endpoints
    path(
        "",
        lambda request: render(request, template_name="advertisements/main_page.html/"),
        name="template-mainpage",
    ),
    path(
        "create/ad/",
        render_template.CreateAdTemplate.as_view(),
        name="template-create-ad",
    ),
    path(
        'category/<str:category_name>/',
        lambda request, category_name: render(request, "advertisements/category.html/"),
        name="template-category"
    ),
    path(
        'subcategory/<str:subcategory_name>/',
        lambda request, subcategory_name: render(request, "advertisements/subcategory.html/"),
        name="template-subcategory"
    ),
    path(
        "ad/<int:pk>/",
        lambda request, pk: render(
            request, template_name="advertisements/detail_ad.html/"
        ),
        name="template-detail-ad",
    ),
    # API endpoints
    path(
        "",
        include(router.urls),
    ),
    path(
        "api/v1/sales-mark/",
        views.SalesMarkView.as_view(),
        name="api-sold-mark"
    ),
    path(
        "api/v1/category/<str:category>/",
        views.ListADCategory.as_view(),
        name="api-category",
    ),
    path(
        "api/v1/subcategory/<str:subcategory>/",
        views.ListADSubcategory.as_view(),
        name="api-subcategory",
    ),
]
