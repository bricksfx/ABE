from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


def login(request):
    return render(request, 'User/login.html', {})

def index(request):
    return render(request, 'User/index.html', {})

def upload_file(request):
    return render(request, 'User/upload.html', {})

def download_file(request):
    return render(request, 'User/download.html', {})

def share_file(request):
    return render(request, 'User/share.html', {})

def list_file(request):
    return render(request, 'User/list.html', {})