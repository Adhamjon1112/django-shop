from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Shop, Product
from .forms import ShopForm, ProductForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse


class MainIndex(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:shop_create')  
            else:
                messages.error(request, "Noto'g'ri username yoki parol")
        
        return self.render_to_response({'form': form})


class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'main/shop_form.html'
    success_url = reverse_lazy('main:product_create')  

    def form_valid(self, form):
        # Tizimga kirgan foydalanuvchini shop'ga bog'lash
        form.instance.user = self.request.user
        form.instance.status = 0  # Yangi shop - tasdiqlanmagan
        messages.success(self.request, "Magazin qo'shildi. Admin tasdiqlashi kerak.")
        return super().form_valid(form)



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        try:
            # shop = Shop.objects.get(user=self.request.user, status=2)
            form.instance.shop = form.cleaned_data['shop']
            form.instance.status = 0  # Yangi mahsulot
            messages.success(self.request, "Mahsulot qo'shildi. Admin tasdiqlashi kerak.")
            return super().form_valid(form)
        except Shop.DoesNotExist:
            form.add_error(None, "Tasdiqlangan magaziningiz yo'q. Admin tasdiqlashini kuting.")
            return self.form_invalid(form)
        
    def get_success_url(self):
        # Qo'shilgan mahsulotning shop_id si bo'yicha API yo'nalishiga yo'naltirish
        return reverse('api:approved_products', kwargs={'shop_id': self.object.shop.id})