import os
import re
import datetime

from django.http import HttpResponse

from .models import NginxLog


# Define Django project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Define text file name
filename = 'access.log'
# Define the full file path
# filepath = BASE_DIR + '/static_cdn/media_root/resume/' + filename
filepath = BASE_DIR + '/static/log/' + filename

def parser(request):

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