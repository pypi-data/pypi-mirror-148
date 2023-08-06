from django.http import JsonResponse

from nwon_django_toolbox.exception_handler.get_response import (
    get_response as get_response_from_handler,
)


class ExceptionMiddleware(object):
    def __init__(self, get_response=get_response_from_handler):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 500:
            response = self.get_response(
                message="Internal server error, please try again later",
                status_code=response.status_code,
            )
            return JsonResponse(response, status=response["status_code"])

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = self.get_response(
                message="Page not found, invalid url", status_code=response.status_code
            )
            return JsonResponse(response, status=response["status_code"])

        return response
