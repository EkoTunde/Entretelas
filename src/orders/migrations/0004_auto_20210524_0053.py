# Generated by Django 2.2.2 on 2021-05-24 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210522_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='fabrics',
        ),
        migrations.AddField(
            model_name='fabric',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fabrics', to='orders.Order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='expiration_date',
            field=models.DateField(default=None, verbose_name='Fecha de expiración'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_edited',
            field=models.DateTimeField(auto_now=True, verbose_name='Última edición'),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('NE', 'Nuevo'), ('ER', 'Esperando respuesta'), ('AC', 'Aceptado'), ('MK', 'En confección'), ('FI', 'Terminado')], default='NE', max_length=1, verbose_name='Estado'),
        ),
    ]