from django.core.cache import cache
from django.http import HttpResponse

class LoginRateLimitMiddleware:
    limit = 8
    window = 300

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower()
        protected = request.method == "POST" and any(part in path for part in ("/login", "/signin", "/admin"))
        key = None
        if protected:
            remote = request.META.get("REMOTE_ADDR", "")
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
            ip = forwarded.split(",", 1)[0].strip() if remote in {"127.0.0.1", "::1"} and forwarded else remote
            key = f"login-attempt:{ip}:{path[:120]}"
            if int(cache.get(key, 0)) >= self.limit:
                response = HttpResponse("Too many login attempts. Try again in 5 minutes.", status=429)
                response["Retry-After"] = str(self.window)
                return response
        response = self.get_response(request)
        if protected and key:
            if 300 <= response.status_code < 400:
                cache.delete(key)
            elif response.status_code < 500:
                try:
                    cache.incr(key)
                except ValueError:
                    cache.set(key, 1, self.window)
        return response

