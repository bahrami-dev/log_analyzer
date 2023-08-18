from django.db import models


class LogFile(models.Model):
    name =  models.CharField(max_length=256, unique=True)
    original_name = models.CharField(max_length=256)
    file = models.FileField(upload_to="logs")
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

class NginxLog(models.Model):
    ip_address = models.CharField(max_length=32)
    remote_user = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    request_method = models.CharField(max_length=20)
    request_url = models.TextField()
    protocol = models.CharField(max_length=20)
    status_code = models.IntegerField()
    size_of_response_body = models.BigIntegerField()
    referrer_url = models.TextField()
    user_agent = models.TextField()

