from django.contrib import admin

from .models import LogFile, NginxLog

admin.site.register(LogFile)
admin.site.register(NginxLog)
