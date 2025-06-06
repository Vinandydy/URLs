# Generated by Django 5.2 on 2025-04-18 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='Наименование')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Иконка')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Сайт',
                'verbose_name_plural': 'Сайты',
                'db_table': 'url',
            },
        ),
    ]
