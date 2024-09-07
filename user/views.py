import random

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from user.forms import PasswordResetForm, PasswordResetRequestForm, RegisterForm, UserRegisterConfirmForm
from user.models import User


class UserRegister(TemplateView):
    template_name = 'user/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            request.session['register_data'] = form.cleaned_data
            code = random.randint(1000000, 9999999)
            request.session['code'] = code
            
            # form.save(commit=True)
            # send_sms(forms.cleaned_data['username'], code)
            messages.success(request, "SMS xabar tasdiqlash kodi bilan kiritilgan telefon raqamga jo'natildi")
            return redirect('user:register-confirm')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UserRegister, self).get_context_data(**kwargs)
        context['form'] = RegisterForm()
        context["title"] = "Ro'yxatdan o'tish"

        return context

class UserRegisterConfirm(TemplateView):
    template_name = 'user/register-confirm.html'

    def dispatch(self, request, *args, **kwargs):
        data = self.request.session.get('register_data')
        if data is None:
            raise Http404

        return super(UserRegisterConfirm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserRegisterConfirmForm(request, data=request.POST)
        if form.is_valid():
            data = self.request.session.get('register_data')
            del data['confirm']
            
            user = User(**data)
            user.set_password(data['password'])
            user.save()
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz")
            request.session['register_data'] = None
            request.session['code'] = None

            return redirect('main:index')

        context = self.get_context_data()
        context['form'] = form
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        messages.info(self.request, f"code is: {self.request.session.get('code')}")

        context = super(UserRegisterConfirm, self).get_context_data(**kwargs)

        context['form'] = UserRegisterConfirmForm(self.request)
        context['title'] = "Tasdiqlash"
        return context


class PasswordResetRequestView(TemplateView):
    template_name = 'user/password_reset_request.html'

    def post(self, request, *args, **kwargs):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                form.add_error('username', "Bunday foydalanuvchi topilmadi.")
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return self.render_to_response(context)

            
            code = random.randint(100000, 999999)
            request.session['reset_code'] = code
            request.session['reset_user_id'] = user.id
            
            messages.info(self.request, f"code is: {self.request.session.get('reset_code')}")
            return redirect('user:password_reset_confirm')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PasswordResetRequestView, self).get_context_data(**kwargs)
        context['form'] = PasswordResetRequestForm()
        return context
    
class PasswordResetConfirmView(TemplateView):
    template_name = 'user/password_reset_confirm.html'

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST, request=request)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user_id = request.session.get('reset_user_id')
            
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Parolingiz muvaffaqiyatli o`zgartirildi!")
                request.session.pop('reset_user_id', None)
                request.session.pop('reset_code', None)
                return redirect('main:index')
            except User.DoesNotExist:
                form.add_error('new_password', "Foydalanuvchi topilmadi.")

        return self.render_to_response({'form': form})

    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordResetForm()
        return context