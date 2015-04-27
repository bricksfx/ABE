#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from User.models import MyUser
from django import forms


# Create your views here.
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        return HttpResponse("登录成功")
    return render(request, 'User/login.html', {'form': form})


@login_required(login_url='/login/')
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