# Generated by Django 2.2.8 on 2020-10-10 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image_artist',
            field=models.ImageField(default='https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/12.jpg', upload_to='images/'),
        ),
    ]
