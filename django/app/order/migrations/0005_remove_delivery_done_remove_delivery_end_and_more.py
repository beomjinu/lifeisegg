# Generated by Django 4.2.2 on 2023-07-07 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_delivery_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='done',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='end',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='start',
        ),
    ]
