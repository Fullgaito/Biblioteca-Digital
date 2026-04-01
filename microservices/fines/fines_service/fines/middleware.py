from django.http import JsonResponse
import os

class InternalAPIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-Internal-API-Key')
        expected_key = os.getenv('INTERNAL_API_KEY')

        if api_key != expected_key:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        response = self.get_response(request)
        return response