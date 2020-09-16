# Generated by Django 3.0.6 on 2020-09-12 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_auto_20200912_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default='0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(default='10', on_delete=django.db.models.deletion.CASCADE, to='Main.Coupon'),
            preserve_default=False,
        ),
    ]
