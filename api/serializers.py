from rest_framework import serializers
from main.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'shop', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'quantity']
