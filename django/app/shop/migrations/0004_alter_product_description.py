# Generated by Django 4.2.2 on 2023-07-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_og_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]