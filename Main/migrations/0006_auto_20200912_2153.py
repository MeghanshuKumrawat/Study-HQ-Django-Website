# Generated by Django 3.0.6 on 2020-09-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20200912_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(blank=True, default=10, null=True),
        ),
    ]