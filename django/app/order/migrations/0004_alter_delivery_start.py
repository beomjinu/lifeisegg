# Generated by Django 4.2.2 on 2023-07-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_delivery_end_delivery_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='start',
            field=models.DateField(),
        ),
    ]
