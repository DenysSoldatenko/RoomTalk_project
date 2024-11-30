from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world. You're at the polls home view.")

def room(request):
    return HttpResponse("Hello, world. You're at the polls room view.")