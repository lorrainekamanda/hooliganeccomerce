# Generated by Django 2.2.8 on 2020-11-08 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
