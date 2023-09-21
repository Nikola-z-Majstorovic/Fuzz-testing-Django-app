
import logging

logger = logging.getLogger(__name__)


class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        logger.info("bla bla processing request")
        print(request.META)
        print(type(request))
        # print(f"request {request.META['header']}")
        response = self.get_response(request)
        logger.info(f"bla bla processing response  {response.status_code} {response.content} ")
        return response

    def process_request(self, request):
        self.logger.info(f"Request: {request.method} {request.path} ")
        # self.logger.info('Request', extra={'httprequest_method': request.method})

    def process_response(self, request, response):
        self.logger.info('Response', extra={'httpresponse_status_code': response.status_code})
        return response