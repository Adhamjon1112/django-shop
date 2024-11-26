import random
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, Shop, Product, Card
from .forms import ConfirmSMSForm, OrderForm, ShopForm, ProductForm, CardForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated

from django.views.generic import TemplateView, FormView, ListView

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


class ShopCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'main/shop_form.html'
    success_url = reverse_lazy('main:product_create')  
    permission_required = 'main.add_shop'  
    
    def form_valid(self, form):
        
        # Tizimga kirgan foydalanuvchini shop'ga bog'lash
        form.instance.user = self.request.user
        form.instance.status = 0  # Yangi shop - tasdiqlanmagan
        messages.success(self.request, "Magazin qo'shildi. Admin tasdiqlashi kerak.")
        return super().form_valid(form)



class ProductCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    permission_required = 'main.add_product'

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
        return reverse('api:approved_product', kwargs={'shop_id': self.object.shop.id})

class UserProductsView(TemplateView):
    template_name = 'main/products.html'

    def get_context_data(self, **kwargs):
        context = super(UserProductsView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(status=Product.STATUS_APPROVED)
        return context
    
class PurchaseProductView(LoginRequiredMixin, FormView):
    template_name = 'main/purchase_product.html'
    form_class = OrderForm

    def get_product(self, product_id):
        return get_object_or_404(Product, id=product_id, status=2)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # user ni formga o'tkazamiz
        return kwargs

    def form_valid(self, form):
        product = self.get_product(self.kwargs['product_id'])
        quantity = form.cleaned_data['quantity']

        if product.quantity < quantity:
            messages.error(self.request, "Kechirasiz, mahsulot miqdori yetarli emas.")
            return self.form_invalid(form)

        product.quantity -= quantity
        product.save()
        order = form.save(commit=False)
        order.user = self.request.user
        order.product = product
        order.save()

        sms_code = str(random.randint(100000, 999999))
        self.request.session['sms_code'] = sms_code

        messages.success(self.request, "Tasdiqlash kodi yuborildi!")
        messages.info(self.request, f"SMS tasdiqlash kodi: {sms_code}")

        return redirect('main:confirm_purchase', order_id=order.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_product(self.kwargs['product_id'])
        return context


class ConfirmPurchaseView(LoginRequiredMixin, FormView):
    template_name = 'main/confirm_purchase.html'
    form_class = ConfirmSMSForm

    def get_order(self, order_id):
        return get_object_or_404(Order, id=order_id, user=self.request.user, is_confirmed=False)

    def form_valid(self, form):
        order = self.get_order(self.kwargs['order_id'])
        sms_code = self.request.session.get('sms_code')

        if form.cleaned_data['sms_code'] == sms_code:
            order.is_confirmed = True
            order.save()
            messages.success(self.request, "Mahsulot muvaffaqiyatli sotib olindi!")
            return redirect('main:products')
        else:
            messages.error(self.request, "Kod noto‘g‘ri. Qayta urinib ko‘ring.")
            return redirect('main:confirm_purchase', order_id=order.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_order(self.kwargs['order_id'])
        return context

class AddCardView(LoginRequiredMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'main/add_card.html'
    success_url = reverse_lazy('main:products')

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'main/card_list.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
    



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Article
# from .serializers import ArticleSerializer

# class ArticleAPIView(APIView):
#     def get(self, request, pk=None):
#         if pk:
#             try: 
#                 article = Article.objects.get(pk=pk)
#                 serializer = ArticleSerializer(article)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Article.DoesNotExist:
#                 return Response({"Error": 'Article not found'}, status = status.HTTP_404_NOT_FOUND)
        
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = ArticleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk):
#         try:
#             article = Article.objects.get(pk=pk)
#         except Article.DoesNotExist:
#             return Response({'Error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ArticleSerializer(article, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         try:
#             article = Article.objects.get(pk=pk)
#         except Article.DoesNotExist:
#             return Response({'Error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ArticleSerializer(article, data = request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             article = Article.objects.get(pk=pk)
#             article.delete()
#             return Response({'Error': 'Article deleted'}, status=status.HTTP_204_NO_CONTENT)
#         except Article.DoesNotExist:
#             return Response({'Error': 'Article article not found'}, status=status.HTTP_404_NOT_FOUND)
                                