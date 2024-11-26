from rest_framework import serializers
from main.models import Product, Shop

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'shop', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'quantity', 'price']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['user', 'id', 'name_uz', 'name_ru', 'name_en']