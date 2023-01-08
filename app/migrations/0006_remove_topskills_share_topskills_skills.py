# Generated by Django 4.1.5 on 2023-01-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_topskills_alter_citysharestatistics_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topskills',
            name='share',
        ),
        migrations.AddField(
            model_name='topskills',
            name='skills',
            field=models.TextField(default='', verbose_name='Топ-10 навыков'),
        ),
    ]
