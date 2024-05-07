from django.http import HttpResponse

def index(request) :
    print("view가 실행되는 중")
    return HttpResponse("Hello, world.")