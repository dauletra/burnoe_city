# Generated by Django 3.0.4 on 2020-05-07 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burnoe_app', '0013_auto_20200504_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='Заголовок')),
                ('link', models.URLField()),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
            ],
        ),
    ]