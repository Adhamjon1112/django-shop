from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    STATUS_CHOICES = (
        (0, 'Yangi'),
        (1, 'Tasdiqlanmagan'),
        (2, 'Tasdiqlangan'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name_uz = models.CharField(max_length=50, verbose_name="Magazin nomi (UZ)")
    name_ru = models.CharField(max_length=50, verbose_name="Magazin nomi (RU)")
    name_en = models.CharField(max_length=50, verbose_name="Magazin nomi (EN)")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Holati")

    def __str__(self):
        return self.name_uz

class Product(models.Model):
    STATUS_CHOICES = (
        (0, 'Yangi'),
        (1, 'Tasdiqlanmagan'),
        (2, 'Tasdiqlangan'),
    )

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
