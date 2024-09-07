from django.urls import path
from .views import ProductListView

app_name = 'api'

urlpatterns = [
    path('products/<int:shop_id>/', ProductListView.as_view(), name='approved_products'),
]
