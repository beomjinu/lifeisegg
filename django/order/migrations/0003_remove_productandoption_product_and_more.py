# Generated by Django 4.2.2 on 2023-06-14 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_detail_address_order_delivery_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productandoption',
            name='product',
        ),
        migrations.AddField(
            model_name='productandoption',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
    ]