from django.http import render
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def vsem_privet(request):
    return HttpResponse("Всем привет")
