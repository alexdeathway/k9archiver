import time
import threading
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404
from django.urls import resolve, Resolver404
from django.core.exceptions import PermissionDenied

class CacheIfSlowMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        #no cache of auth related views 
        if request.user.is_authenticated or request.path in ['/signup/', '/login/']:
            return None

        request.start_time = time.time()
        cache_key = f'cache_{request.path}'
        old_cache_key = f'old_cache_{request.path}'

        cached_response_content = cache.get(old_cache_key)
        if cached_response_content:
            request.cached_response = HttpResponse(cached_response_content)

        request.view_args = view_args
        request.view_kwargs = view_kwargs

        try:
            request.view_name = resolve(request.path).view_name
        except Resolver404:
            request.view_name = None

    def process_response(self, request, response):
        if request.user.is_authenticated or request.path in ['/signup/', '/login/'] or response.status_code == 404:
            return response

        elapsed_time = (time.time() - request.start_time) * 1000
        cache_key = f'cache_{request.path}'
        old_cache_key = f'old_cache_{request.path}'

        if elapsed_time > 100:
            if hasattr(request, 'cached_response'):
                threading.Thread(
                    target=self.regenerate_cache,
                    args=(request.path, request.view_name, request.view_args, request.view_kwargs)
                ).start()
                return request.cached_response

            cache.set(old_cache_key, response.content, timeout=None) #old persistent cache
            cache.set(cache_key, response.content, timeout=3600)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, (Http404, PermissionDenied)):
            return None
        return None

    def regenerate_cache(self, path, view_name, view_args, view_kwargs):
        if not view_name:
            return

        from django.test.client import RequestFactory
        from django.template.response import SimpleTemplateResponse

        request = RequestFactory().get(path)
        view = resolve(path).func

        response = view(request, *view_args, **view_kwargs)

        if isinstance(response, SimpleTemplateResponse):
            response.render()

        cache_key = f'cache_{path}'
        old_cache_key = f'old_cache_{path}'
        cache.set(old_cache_key, response.content, timeout=None)
        cache.set(cache_key, response.content, timeout=3600)
