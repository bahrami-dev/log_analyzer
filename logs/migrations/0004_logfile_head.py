# Generated by Django 4.1.6 on 2023-09-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_nginxlog_log_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfile',
            name='head',
            field=models.IntegerField(default=0),
        ),
    ]
