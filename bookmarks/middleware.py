import logging
import ecs_logging
import time

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

        self.logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler('log/debug.json')
        handler.setFormatter(ecs_logging.StdlibFormatter())
        self.logger.addHandler(handler)

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)

        duration = time.time() - start_time
        if str(response.status_code).startswith('2'):
            self.logger.info("Success",
                             extra={"middleware": type(self).__name__,
                                    'agent.id': request.user.id,
                                    "http.request.method": request.method,
                                    'http.response.status_code': response.status_code,
                                    'url.path': request.build_absolute_uri(),
                                    'http.request.body.content':  request.body.decode('UTF-8')
                                    if request.method != 'POST' else '',
                                    'http.response.body.content': response.content if request.META.get('HTTP_ACCEPT')
                                    .split(',')[0] == 'text/html' else '',
                                    'user_agent.name': request.META['HTTP_USER_AGENT'],
                                    'netflow.procera_http_file_length': len(response.content)
                                    if request.META.get('HTTP_ACCEPT')
                                    .split(',')[0] == 'text/html' else 0,
                                    'checkpoint.content_type':  request.META['CONTENT_TYPE']
                                    if 'CONTENT_TYPE' in request.META else '',
                                    'checkpoint.cookie': request.META['CSRF_COOKIE']
                                    if 'CSRF_COOKIE' in request.META else '',
                                    'rsa.time.duration_time': float(duration),
                                    })
        elif str(response.status_code).startswith('3'):
            self.logger.info("Redirection",
                             extra={"middleware": type(self).__name__,
                                    'agent.id': request.user.id,
                                    "http.request.method": request.method,
                                    'http.response.status_code': response.status_code,
                                    'url.path': request.build_absolute_uri(),
                                    'http.request.body.content': request.body.decode('UTF-8')
                                    if request.method != 'POST' else '',
                                    'http.response.body.content': response.content if request.META.get('HTTP_ACCEPT')
                                    .split(',')[0] == 'text/html' else '',
                                    'user_agent.name': request.META['HTTP_USER_AGENT'],
                                    'netflow.procera_http_file_length': len(response.content)
                                    if request.META.get('HTTP_ACCEPT')
                                    .split(',')[0] == 'text/html' else 0,
                                    'checkpoint.content_type': request.META['CONTENT_TYPE']
                                    if 'CONTENT_TYPE' in request.META else '',
                                    'checkpoint.cookie': request.META['CSRF_COOKIE']
                                    if 'CSRF_COOKIE' in request.META else '',
                                    'rsa.time.duration_time': float(duration),
                                    })
        elif str(response.status_code).startswith('4'):
            self.logger.warning("Client errors",
                                extra={"middleware": type(self).__name__,
                                       'agent.id': request.user.id,
                                       "http.request.method": request.method,
                                       'http.response.status_code': response.status_code,
                                       'url.path': request.build_absolute_uri(),
                                       'http.request.body.content':  request.body.decode('UTF-8')
                                       if request.method != 'POST' else '',
                                       'user_agent.name': request.META['HTTP_USER_AGENT'],
                                       'netflow.procera_http_file_length': len(response.content)
                                       if request.META.get('HTTP_ACCEPT')
                                       .split(',')[0] == 'text/html' else 0,
                                       'checkpoint.content_type': request.META['CONTENT_TYPE']
                                       if 'CONTENT_TYPE' in request.META else '',
                                       'checkpoint.cookie': request.META['CSRF_COOKIE']
                                       if 'CSRF_COOKIE' in request.META else '',
                                       'rsa.time.duration_time': float(duration),
                                       })
        elif str(response.status_code).startswith('5'):
            self.logger.exception("Server errors",
                                  extra={"middleware": type(self).__name__,
                                         'agent.id': request.user.id,
                                         "http.request.method": request.method,
                                         'http.response.status_code': response.status_code,
                                         'url.path': request.build_absolute_uri(),
                                         'http.request.body.content':  request.body.decode('UTF-8')
                                         if request.method != 'POST' else '',
                                         'user_agent.name': request.META['HTTP_USER_AGENT'],
                                         'netflow.procera_http_file_length': len(response.content)
                                         if request.META.get('HTTP_ACCEPT')
                                         .split(',')[0] == 'text/html' else 0,
                                         'checkpoint.content_type': request.META['CONTENT_TYPE']
                                         if 'CONTENT_TYPE' in request.META else '',
                                         'checkpoint.cookie': request.META['CSRF_COOKIE']
                                         if 'CSRF_COOKIE' in request.META else '',
                                         'rsa.time.duration_time': float(duration),
                                         },
                                  exc_info=True)
        return response
