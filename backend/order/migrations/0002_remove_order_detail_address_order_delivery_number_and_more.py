# Generated by Django 4.2.2 on 2023-06-14 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='detail_address',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_number',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('WFP', 'WAITING_FOR_PAYMENT'), ('DP', 'DONE_PAYMENT'), ('IPD', 'IN_PROGRESS_DELIVERY'), ('DD', 'DONE_DELIVERY'), ('C', 'CANCLED')], max_length=99),
        ),
        migrations.AlterField(
            model_name='productandoption',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_and_options', to='order.order'),
        ),
    ]