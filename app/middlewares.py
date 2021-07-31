from django.shortcuts import render

def underconstructionmiddleware(get_response):
    
    def middleware(request):
        response  = render(request, 'app/mysite.html')
        return response

    return middleware

def session_expired_middleware(get_response):

    def middleware(request):
        request.session.set_expiry(0)
        response = get_response(request)
        return response

    return middleware
