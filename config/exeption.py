import datetime
from abc import ABC

import pytz
from pip._internal import req
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from config.loggers import CustomLogger
logger = CustomLogger("api_exceptions")


def custom_exception_handler(exc, context):
    res = exception_handler(exc, context)
    request = context["request"]
    if getattr(exc, "log_exception", False):
        full_url = request.build_absolute_uri()
        base_url = request.build_absolute_uri('/')[:-1]  # Get the base URL without the trailing slash
        path = full_url.replace(base_url, '')

        tehran_timezone = pytz.timezone("Asia/Tehran")
        start_time = datetime.datetime.now(tehran_timezone)
        end_time = datetime.datetime.now(tehran_timezone)

        ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

        user = "AnonymousUser" if not request.user.is_authenticated else request.user.username

        logger.info(
            f"started_time: {start_time} ** method: {request.method} ** status: {exc.status_code} ** {exc.default_code} ** user_posted_data:{request.data} ** {base_url} ** {path} ** user: {user} ** IP: {ip_address} ** time_took: {(end_time - start_time).total_seconds()}")
    return res

class CustomAPIException(APIException, ABC):
    status_code = NotImplemented
    default_code = NotImplemented
    default_detail = NotImplemented
    log_exception = True


class PriceNotFound(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "PriceNotFound"
    default_detail = {"NotFound": "Price didn't filled", "object": "Price"}


class CantUpdate(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "Cant_update"
    default_detail = {"NotFound": "cant update", "object": "Price"}


class CantDelete(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "Cant_delete"
    default_detail = {"NotFound1": "cant delete", "object": "Price"}

