# Generated by Django 2.2.2 on 2021-05-28 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('costs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('making_cost', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='Costo confección')),
                ('making_multiplier', models.CharField(choices=[('H', 'Alto'), ('W', 'Ancho'), ('P', 'Perímetro'), ('NA', 'Nada')], default='NA', max_length=2)),
                ('making_factor', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('making_tolerance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('multiplier_1', models.CharField(choices=[('H', 'Alto'), ('W', 'Ancho'), ('P', 'Perímetro'), ('NA', 'Nada')], default='NA', max_length=2)),
                ('factor_1', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('tolerance_1', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('multiplier_2', models.CharField(choices=[('H', 'Alto'), ('W', 'Ancho'), ('P', 'Perímetro'), ('NA', 'Nada')], default='NA', max_length=2)),
                ('factor_2', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('tolerance_2', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('multiplier_3', models.CharField(choices=[('H', 'Alto'), ('W', 'Ancho'), ('P', 'Perímetro'), ('NA', 'Nada')], default='NA', max_length=2)),
                ('factor_3', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('tolerance_3', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=50, null=True)),
                ('material_1', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_raw_material_comp_1', to='costs.Cost', verbose_name='Materia prima componente 1')),
                ('material_2', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_raw_material_comp_2', to='costs.Cost', verbose_name='Materia prima componente 2')),
                ('material_3', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prod_raw_material_comp_3', to='costs.Cost', verbose_name='Materia prima componente 3')),
            ],
        ),
    ]
