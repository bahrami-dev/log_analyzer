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

from .models import LogFile, NginxLog


# Define Django project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the full file path
last_model_instance = LogFile.objects.last()
last_file_name = last_model_instance.file.name
filepath = BASE_DIR + '/media/' + last_file_name

def parser():

    # Open the log file
    with open(filepath, 'r') as f:

        # Create a regular expression to match the log format
        regex = re.compile(r'^(\S+) - (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) ([\Ss ]+)')

        # Iterate over the lines in the file
        for line in f:

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
                )
    
    return HttpResponse('Done!')


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        # Get the file from the request.
        file = request.FILES['file']
        name = uuid.uuid4().hex
        # Save the file to the database.
        try:
            myfile = File(file)
            log_file = LogFile(
                name=name,
                original_name=file.name,
                file=myfile, 
                size=file.size,
            )
            log_file.save()
            parser()
            return Response({'message': 'File uploaded successfully.'})
        except Exception as e:
            logging.exception(e)
            return Response({'message': 'Uploading Faild.'})