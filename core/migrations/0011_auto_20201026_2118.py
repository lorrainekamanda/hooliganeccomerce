# Generated by Django 2.2.8 on 2020-10-26 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20201026_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='tag',
            new_name='slug',
        ),
    ]
