from django.shortcuts import redirect


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if '/projects/' in request.path and '_email' not in request.path:
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.is_subscribe:
                return redirect('index')

        return response
