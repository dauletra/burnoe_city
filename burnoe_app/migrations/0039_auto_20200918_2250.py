# Generated by Django 3.0.4 on 2020-09-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0038_tag_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['category']},
        ),
        migrations.AddField(
            model_name='tag',
            name='is_displayed',
            field=models.BooleanField(default=False, verbose_name='Показать?'),
        ),
    ]
