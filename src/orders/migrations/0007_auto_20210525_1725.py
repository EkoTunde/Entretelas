# Generated by Django 2.2.2 on 2021-05-25 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210524_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='component_1_raw_material',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_raw_material_comp_1', to='costs.Cost', verbose_name='Materia prima componente 1'),
        ),
        migrations.AlterField(
            model_name='item',
            name='component_2_raw_material',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_raw_material_comp_2', to='costs.Cost', verbose_name='Materia prima componente 2'),
        ),
        migrations.AlterField(
            model_name='item',
            name='component_3_raw_material',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_raw_material_comp_3', to='costs.Cost', verbose_name='Materia prima componente 3'),
        ),
        migrations.AlterField(
            model_name='item',
            name='making_cost',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_making_cost', to='costs.Cost', verbose_name='Costo confección'),
        ),
    ]
