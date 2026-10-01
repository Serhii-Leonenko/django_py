import time
import uuid


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get('X-Request-ID') or uuid.uuid4()

        start_time = time.perf_counter()

        response = self.get_response(request)

        execution_time = (time.perf_counter() - start_time) * 1000

        response['X-Request-ID'] = request_id
        response['X-Response-Time'] = f'{execution_time:.2f}ms'

        return response
