class COOPHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Añadir el encabezado con 'unsafe-none'
        response['Cross-Origin-Opener-Policy'] = 'unsafe-none'
        return response
