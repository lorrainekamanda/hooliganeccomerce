# Generated by Django 2.2.8 on 2020-12-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_paymentdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='time_stamp',
            field=models.DateTimeField(),
        ),
    ]
