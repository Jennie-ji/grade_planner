from django.shortcuts import render
from django.http.response import HttpResponse

def home(request):
    return render(request, 'app_grade/index.html')

# Create your views here.
