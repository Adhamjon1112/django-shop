from django.http import HttpResponseForbidden
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from main.models import Product

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyalangan foydalanuvchilar uchun
     
    
    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')  # URLdan shop_id ni olish
        # Faqat tasdiqlangan mahsulotlarni qaytarish
        return Product.objects.filter(shop_id=shop_id, status=2)
     
    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('main.view_product'):
            return HttpResponseForbidden("Sizda mahsulotlarni ko‘rish huquqi yo‘q")
        else:
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response({'detail': 'Hech qanday tasdiqlangan mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
