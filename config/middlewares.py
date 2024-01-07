import base64
import datetime
import json
import os

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection
from django.http import HttpResponse
from django.urls import resolve
# import django_
import pytz
from rest_framework.response import Response

from config.loggers import CustomLogger


# logs format: request method**status_code**base_url**request_path**user**ip**process_time

class APILoggerMiddleware:
    def __init__(self, get_response, file_name="default_name"):
        # Changing the file name will create a new file.
        self.get_response = get_response
        self.file_name = file_name
        self.logger = self.setup_logger(self.file_name)

    def __call__(self, request):
        tehran_timezone = pytz.timezone("Asia/Tehran")
        start_time = datetime.datetime.now(tehran_timezone)
        response = self.get_response(request)
        end_time = datetime.datetime.now(tehran_timezone)

        user = "AnonymousUser"
        if request.user.is_authenticated:
            user = request.user.national_code
        ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
        full_url = request.build_absolute_uri()
        base_url = request.build_absolute_uri('/')[:-1]  # Get the base URL without the trailing slash
        path = full_url.replace(base_url, '')
        start_time_str = start_time.isoformat()

        # maybe there is some problem in validating data :
        try:
            validate_data = str(response.data)
            self.logger.info(
                f"{start_time_str} ** {request.method} ** {response.status_code} ** validated_post_data: {validate_data} ** {base_url} ** {path} ** {user} ** {ip_address} ** {(end_time - start_time).total_seconds()}")

        except:
            self.logger.info(
                f"{start_time_str} ** {request.method} ** {response.status_code} ** can't log! ** {base_url} ** {path} ** {user} ** {ip_address} ** {(end_time - start_time).total_seconds()}")
        return response

    def setup_logger(self, file_name: str):
        logger = CustomLogger(file_name)

        return logger

    # If DEBUG is true, we're in dev. Raise MiddlewareNotUsed to remove
    # this middleware from the list.
    # TODO: This should probably be based off of the QA env once we hit
    # production
    # if settings.DEBUG:
    #     raise MiddlewareNotUsed


