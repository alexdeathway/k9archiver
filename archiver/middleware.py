# middleware.py
import time
import threading
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.urls import resolve

class CacheIfSlowMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.start_time = time.time()
        cache_key = f'cache_{request.path}'
        old_cache_key = f'old_cache_{request.path}'

        # Check if there's a cached response
        cached_response_content = cache.get(old_cache_key)
        if cached_response_content:
            # Wrap the cached content in an HttpResponse
            request.cached_response = HttpResponse(cached_response_content)

        # Store view args and kwargs for later use
        request.view_args = view_args
        request.view_kwargs = view_kwargs
        request.view_name = request.resolver_match.view_name

    def process_response(self, request, response):
        elapsed_time = (time.time() - request.start_time) * 1000
        cache_key = f'cache_{request.path}'
        old_cache_key = f'old_cache_{request.path}'

        if elapsed_time > 100:
            # Serve the last saved cache immediately if it exists
            if hasattr(request, 'cached_response'):
                # Start a background thread to regenerate the cache
                threading.Thread(
                    target=self.regenerate_cache,
                    args=(request.path, request.view_name, request.view_args, request.view_kwargs)
                ).start()
                return request.cached_response

            # If no cache was served, cache the current response and also save it as the old cache
            # one cache is permanent and the other is temporary
            cache.set(old_cache_key, response.content, timeout=None)  # Save a permanent cache copy
            cache.set(cache_key, response.content, timeout=3600)  # Newer version with timeout

        return response

    def regenerate_cache(self, path, view_name, view_args, view_kwargs):
        from django.test.client import RequestFactory
        from django.template.response import SimpleTemplateResponse

        
        request = RequestFactory().get(path)
        view = resolve(path).func       
        response = view(request, *view_args, **view_kwargs)

        
        if isinstance(response, SimpleTemplateResponse):
            response.render()

        cache_key = f'cache_{path}'
        old_cache_key = f'old_cache_{path}'
        cache.set(old_cache_key, response.content, timeout=None)  # Overwrite old cache permanently
        cache.set(cache_key, response.content, timeout=3600)  # Update the newer version with timeout