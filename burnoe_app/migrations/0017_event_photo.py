# Generated by Django 3.0.4 on 2020-05-13 10:43

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0016_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
    ]