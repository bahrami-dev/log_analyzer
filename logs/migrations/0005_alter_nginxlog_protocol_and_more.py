# Generated by Django 4.1.6 on 2023-10-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_logfile_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginxlog',
            name='protocol',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='nginxlog',
            name='request_method',
            field=models.TextField(),
        ),
    ]
