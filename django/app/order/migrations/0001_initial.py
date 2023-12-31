# Generated by Django 3.2.15 on 2023-06-29 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=99, null=True)),
                ('orderer_name', models.CharField(max_length=99)),
                ('orderer_number', models.CharField(max_length=99)),
                ('orderer_email', models.EmailField(max_length=99)),
                ('recipient_name', models.CharField(max_length=99)),
                ('recipient_number', models.CharField(max_length=99)),
                ('address', models.CharField(max_length=99)),
                ('request', models.CharField(blank=True, max_length=99, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivery', models.CharField(blank=True, max_length=99, null=True)),
                ('status', models.CharField(choices=[('WFP', 'WAITING_FOR_PAYMENT'), ('DP', 'DONE_PAYMENT'), ('IPD', 'IN_PROGRESS_DELIVERY'), ('DD', 'DONE_DELIVERY'), ('C', 'CANCLED')], max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=99)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
            ],
        ),
    ]
