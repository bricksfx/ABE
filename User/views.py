from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


def login(request):
    return render(request, 'User/login.html', {})

def index(request):
    return render(request, 'User/index.html', {})