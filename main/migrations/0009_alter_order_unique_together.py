# Generated by Django 5.0.3 on 2024-11-07 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_card_order_delete_purchase"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="order",
            unique_together=set(),
        ),
    ]
