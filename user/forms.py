from django import forms
from django.core.exceptions import ValidationError

from user.models import User


class RegisterForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()

        if data.get('password') != data.get('confirm'):
            raise ValidationError({
                "confirm": "Parollar bir xil emas"
            })

        return data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm']
        widgets = {
            'password': forms.PasswordInput
        }


class UserRegisterConfirmForm(forms.Form):
    code = forms.CharField(max_length=10)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        value = self.cleaned_data.get('code')
        code = self.request.session.get('code')
        if value != str(code):
            raise ValidationError("Kiritilgan kod noto'g'ri")

        return value


class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=254, label="Username", help_text=("Required. Telefon raqam"))

class PasswordResetForm(forms.Form):
    code = forms.CharField(max_length=10, label="Code")
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        code = cleaned_data.get('code')

        if new_password != confirm_password:
            raise ValidationError("Parollar bir xil emas")

        
        session_code = self.request.session.get('reset_code')
        if code != str(session_code):
            raise ValidationError("SMS kod noto'g'ri.")

        return cleaned_data