from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def rate_limiting(request):

    request_ip = get_client_ip(request)
    if cache.get(request_ip):
        request_calls = cache.get(request_ip)
        if request_calls >= 5:
            return JsonResponse({'status': 501, 
            'message': 'You have exhausted the limit',
            'time': f'Try after {cache.ttl(request_ip)} seconds'})
        else:
            cache.set(request_ip, request_calls+1)
            return JsonResponse({'status': 200,
            'message': 'You made api call',
            'request_calls': request_calls})

    cache.set(request_ip, 1, timeout=60)
    return JsonResponse({'status': 200, 'ip': get_client_ip(request)})
