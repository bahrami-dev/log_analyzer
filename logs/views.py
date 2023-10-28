import os
import re
import datetime
import uuid
import logging

from django.core.files import File
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import generics
from rest_framework.exceptions import ValidationError, NotFound

from .models import LogFile, NginxLog

from .serializers import NginxLogSerializer, LogFileSerializer

# Define Django project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def parser(filepath, log_file):

    # Open the log file
    with open(filepath, 'r') as f:

        # Create a regular expression to match the log format
        regex = re.compile(r'^(\S+) - (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) ([\Ss ]+)')

        # Iterate over the lines in the file
        line_count = 0
        for line in f:

            line_count += 1 

            if line_count <= log_file.head:
                continue
            # Match the line against the regular expression
            match = regex.match(line)

            # If the line matches the regular expression, extract the fields
            if match:
                ip_address = match.group(1)
                remote_user = match.group(2)
                date_time = match.group(3)
                request_method = match.group(4)
                request_url = match.group(5)
                protocol = match.group(6)
                status_code = match.group(7)
                size_of_response_body = match.group(8)
                referrer_url = match.group(9)
                user_agent = match.group(10)

                # Convert to native format
                format = "%d/%b/%Y:%H:%M:%S %z"
                date_time = datetime.datetime.strptime(date_time, format)
                status_code = int(status_code)
                size_of_response_body = int(size_of_response_body)

                NginxLog.objects.create(
                    ip_address = ip_address,
                    remote_user = remote_user,
                    date_time = date_time,
                    request_method = request_method,
                    request_url = request_url,
                    protocol = protocol,
                    status_code = status_code,
                    size_of_response_body = size_of_response_body,
                    referrer_url = referrer_url,
                    user_agent = user_agent,
                    log_file=log_file
                )

        log_file.head = line_count
        log_file.save()
    
    return HttpResponse('Done!')


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = LogFileSerializer

    def post(self, request):
        # Get the file from the request.
        file = request.FILES['file']
        name = uuid.uuid4().hex
        # Save the file to the database.
        try:
            myfile = File(file)
            log_file = LogFile.objects.create(
                name=name,
                original_name=file.name,
                file=myfile, 
                size=file.size,
            )

            # Define the full file path
            filepath = BASE_DIR + '/media/' + log_file.file.name

            parser(filepath, log_file)
            data = LogFileSerializer(log_file).data
            return Response(data)
        except Exception as e:
            logging.exception(e)
            return Response({'message': 'Uploading Failed.'})
        

class FileUpdateView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = LogFileSerializer
    
    def put(self, request, pk):
        # Get the file from the request.
        file = request.FILES['file']
        try:
            log_file = LogFile.objects.get(id=pk)
        except:
            raise NotFound
        
        try:
            old_file_path = BASE_DIR + '/media/' + log_file.file.name

            log_file.name = uuid.uuid4().hex
            log_file.original_name = file.name
            log_file.file = File(file)
            log_file.size=file.size
            log_file.save()

            remove_old_file(old_file_path)

            # Define the full file path
            filepath = BASE_DIR + '/media/' + log_file.file.name

            parser(filepath, log_file)
            data = LogFileSerializer(log_file).data
            return Response(data)
        except Exception as e:
            logging.exception(e)
            return Response({'message': 'Updating Failed.'})


class Statistics(generics.ListAPIView):
    serializer_class = NginxLogSerializer

    def get_queryset(self):
        queryset = NginxLog.objects.all()
        id = self.kwargs['id']
        key = self.request.query_params.get("key")
        value = self.request.query_params.get("value")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if key is not None and value is not None:
            kwargs = {
                'log_file_id': id,
                '{0}'.format(key): '{0}'.format(value),
            }
            queryset = queryset.filter(**kwargs)

        else:
            queryset = queryset.filter(log_file_id=id)

        if start_date is not None:
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
            except:
                raise ValidationError
            queryset = queryset.filter(date_time__gte=start_date)

        if end_date is not None:
            try:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')
            except:
                raise ValidationError
            queryset = queryset.filter(date_time__lte=end_date)

        return queryset


def remove_old_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        logging.exception("The file does not exist")