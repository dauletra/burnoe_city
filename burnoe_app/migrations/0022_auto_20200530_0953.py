# Generated by Django 3.0.4 on 2020-05-30 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0021_auto_20200530_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='content',
            field=models.TextField(max_length=310, verbose_name='Описание'),
        ),
    ]