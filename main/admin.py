from django.contrib import admin
from main.models import Product, Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name_uz', 'status')
    list_filter = ('status',)
    search_fields = ('name_uz', 'name_ru', 'name_en')
    actions = ['approve_shop', 'mark_as_pending']
    list_per_page = 25

    # Action magazinni tasdiqlash uchun
    def approve_shop(self, request, queryset):
        queryset.update(status=2)  # Tasdiqlangan holatga o'zgartirish
        self.message_user(request, "Tanlangan magazinlar tasdiqlandi.")
    approve_shop.short_description = "Tanlangan magazinlarni tasdiqlash"

    def mark_as_pending(self, request, queryset):
        queryset.update(status=1)
        self.message_user(request, "Tanlangan magazinlar tasdiqlanmadi.")
    mark_as_pending.short_description = "Tanlangan magazinlar tasdiqlanmagan holatga o'tkazish"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'name_uz', 'quantity','status')
    list_filter = ('status',)
    search_fields = ('name_uz', 'name_ru', 'name_en')
    actions = ['approve_product', 'mark_as_pending']
    list_per_page = 25

    
    def approve_product(self, request, queryset):
        queryset.update(status=2)  
        self.message_user(request, "Tanlangan mahsulotlar tasdiqlandi.")
    approve_product.short_description = "Tanlangan mahsulotlarni tasdiqlash"

    def mark_as_pending(self, request, queryset):
        queryset.update(status=1)
        self.message_user(request, "Tanlangan mahsulotlar tasdiqlanmagan holatga o'tkazildi.")
    mark_as_pending.short_description = "Tanlangan mahsulotlarni tasdiqlanmagan holatga o'tkazish"