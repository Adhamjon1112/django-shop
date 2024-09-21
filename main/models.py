from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Shop(models.Model):
    STATUS_NEW = 0
    STATUS_NOT_APPROVED = 1
    STATUS_APPROVED = 2

    STATUS_CHOICES = [
        (STATUS_NEW, _("Yangi")),
        (STATUS_NOT_APPROVED, _("Tasdiqlanmagan")),
        (STATUS_APPROVED, _("Tasdiqlangan")),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name_uz = models.CharField(max_length=50, verbose_name="Magazin nomi (UZ)")
    name_ru = models.CharField(max_length=50, verbose_name="Magazin nomi (RU)")
    name_en = models.CharField(max_length=50, verbose_name="Magazin nomi (EN)")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Holati")

    def __str__(self):
        return self.name_uz

class Product(models.Model):
    STATUS_NEW = 0
    STATUS_NOT_APPROVED = 1
    STATUS_APPROVED = 2

    STATUS_CHOICES = [
        (STATUS_NEW, _("Yangi")),
        (STATUS_NOT_APPROVED, _("Tasdiqlanmagan")),
        (STATUS_APPROVED, _("Tasdiqlangan")),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name="Magazin")
    name_uz = models.CharField(max_length=100, verbose_name="Mahsulot nomi (UZ)")
    name_ru = models.CharField(max_length=100, verbose_name="Mahsulot nomi (RU)")
    name_en = models.CharField(max_length=100, verbose_name="Mahsulot nomi (EN)")
    description_uz = models.TextField(verbose_name="Mahsulot tavsifi (UZ)", blank=True, null=True)
    description_ru = models.TextField(verbose_name="Mahsulot tavsifi (RU)", blank=True, null=True)
    description_en = models.TextField(verbose_name="Mahsulot tavsifi (EN)", blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Holati")
    quantity = models.IntegerField(default=0, verbose_name="Miqdori")

    def __str__(self):
        return self.name_uz
