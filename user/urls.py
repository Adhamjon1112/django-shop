from django.urls import path

from user.views import PasswordResetConfirmView, PasswordResetRequestView, UserRegister, UserRegisterConfirm

app_name = 'user'
urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('register/confirm/', UserRegisterConfirm.as_view(), name='register-confirm'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]