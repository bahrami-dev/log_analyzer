from rest_framework import serializers
from .models import NginxLog, LogFile


class NginxLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NginxLog
        fields = '__all__'


class LogFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogFile
        fields = '__all__'
        read_only_fields = ('name', 'original_name', 'size')