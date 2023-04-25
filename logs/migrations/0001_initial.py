# Generated by Django 4.1.6 on 2023-04-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NginxLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=32)),
                ('remote_user', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField()),
                ('request_method', models.CharField(max_length=20)),
                ('request_url', models.TextField()),
                ('protocol', models.CharField(max_length=20)),
                ('status_code', models.IntegerField()),
                ('size_of_response_body', models.BigIntegerField()),
                ('referrer_url', models.TextField()),
                ('user_agent', models.TextField()),
            ],
        ),
    ]
