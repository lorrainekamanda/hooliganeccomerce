# Generated by Django 2.2.8 on 2020-10-26 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201026_1936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='tag',
            new_name='slug',
        ),
    ]
