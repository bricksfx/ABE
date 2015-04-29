#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from User.models import MyUser
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
@csrf_protect
def Login(request):
    if request.method == 'POST':
        next_url = request.POST['next']

    print request.GET
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print request
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return HttpResponse("您的号被封了, 请联系本站管理员")
        else:
            return HttpResponse("请注册")
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