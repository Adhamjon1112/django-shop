from django.urls import path

from main.views import MainIndex, ProductCreateView, ShopCreateView

app_name = 'main'
urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('shop/create/', ShopCreateView.as_view(), name='shop_create'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
]
