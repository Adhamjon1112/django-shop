from django import forms
from .models import Shop, Product, Card, Order

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name_uz', 'name_ru', 'name_en']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['shop'].queryset = Shop.objects.filter(user=user, status=2)


class OrderForm(forms.ModelForm):
    card = forms.ModelChoiceField(queryset=None, empty_label="Karta tanlang")
    quantity = forms.IntegerField(min_value=1, label="Miqdor", help_text="Sotib olish miqdorini kiriting")

    class Meta:
        model = Order
        fields = ['card', 'quantity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # Foydalanuvchiga tegishli kartalarni filter orqali tanlash imkoniyatini yaratamiz
        self.fields['card'].queryset = Card.objects.filter(user=user)

class ConfirmSMSForm(forms.Form):
    sms_code = forms.CharField(max_length=6, label="Tasdiqlash kodingizni kiriting")


class CardForm(forms.ModelForm):
    # expiry_date = forms.CharField(validators=[validate_expiry_date], widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    
    class Meta:
        model = Card
        fields = ['card_number', 'expiry_date', 'card_holder']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Card Number'}),
            'card_holder': forms.TextInput(attrs={'placeholder': 'Card Holder Name'}),
        }