# Generated by Django 2.2.2 on 2021-06-15 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210601_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Pago', 'verbose_name_plural': 'Pagos'},
        ),
        migrations.AddField(
            model_name='order',
            name='customer_city',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_state',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_zip_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Localidad'),
        ),
    ]
