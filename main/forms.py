from django import forms
from .models import Shop, Product

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name_uz', 'name_ru', 'name_en']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'quantity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Foydalanuvchining tasdiqlangan magazinlarini olish
            self.fields['shop'].queryset = Shop.objects.filter(user=user, status=2)
