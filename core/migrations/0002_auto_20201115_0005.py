# Generated by Django 2.2.8 on 2020-11-15 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='about_your_work',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='focus',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='profession',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
