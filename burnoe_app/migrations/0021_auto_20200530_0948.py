# Generated by Django 3.0.4 on 2020-05-30 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0020_auto_20200528_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='content',
            field=models.TextField(max_length=300, verbose_name='Описание'),
        ),
    ]
