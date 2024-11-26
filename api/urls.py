from django.urls import path
from .views import ProductListView, ProductViewSet, ShopViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Hujjatlari",    # majburiy soha
        default_version='v2',      # majburiy soha
        description="API haqida batafsil ma'lumot",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'api'

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(basename='products', viewset=ProductViewSet, prefix='products')
router.register(basename='shops', viewset=ShopViewSet, prefix='shops')


urlpatterns = [
    path('product/<int:shop_id>/', ProductListView.as_view(), name='approved_product'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
] + router.urls

