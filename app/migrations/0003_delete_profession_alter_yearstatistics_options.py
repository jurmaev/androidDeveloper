# Generated by Django 4.1.5 on 2023-01-07 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_yearstatistics_alter_profession_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profession',
        ),
        migrations.AlterModelOptions(
            name='yearstatistics',
            options={'verbose_name': 'Статистика по годам', 'verbose_name_plural': 'Статистика по годам'},
        ),
    ]
