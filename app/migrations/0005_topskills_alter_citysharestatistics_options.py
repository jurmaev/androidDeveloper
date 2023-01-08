# Generated by Django 4.1.5 on 2023-01-08 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_citysalarystatistics_citysharestatistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('share', models.FloatField(verbose_name='Топ-10 навыков')),
            ],
            options={
                'verbose_name': 'Топ-10 навыков по году',
                'verbose_name_plural': 'Топ-10 навыков по годам',
            },
        ),
        migrations.AlterModelOptions(
            name='citysharestatistics',
            options={'verbose_name': 'Доля вакансий по городу', 'verbose_name_plural': 'Доля вакансий по городам'},
        ),
    ]