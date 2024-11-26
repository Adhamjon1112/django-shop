from django.urls import path

from main.views import AddCardView, CardListView, ConfirmPurchaseView, MainIndex, ProductCreateView, PurchaseProductView, ShopCreateView, UserProductsView

app_name = 'main'
urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('shop/create/', ShopCreateView.as_view(), name='shop_create'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),

    path('products/', UserProductsView.as_view(), name='products'),
    path('purchase/<int:product_id>/', PurchaseProductView.as_view(), name='purchase_product'),
    path('confirm-purchase/<int:order_id>/', ConfirmPurchaseView.as_view(), name='confirm_purchase'),
    path('add-card/', AddCardView.as_view(), name='add_card'),
    path('cards/', CardListView.as_view(), name='card_list'),
]

