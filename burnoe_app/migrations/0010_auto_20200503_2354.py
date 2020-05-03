# Generated by Django 3.0.4 on 2020-05-03 17:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0009_auto_20200503_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['order'], 'verbose_name_plural': 'Product categories'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'ordering': ['order'], 'verbose_name_plural': 'Service categories'},
        ),
        migrations.AddField(
            model_name='contact',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 10, 17, 54, 58, 251173, tzinfo=utc), verbose_name='Дата удаления'),
        ),
    ]
