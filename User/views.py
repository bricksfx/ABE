#coding=utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from User.models import MyUser
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect
from .forms import UploadFileForm, LoginForm
from .file_handle import handle_uploaded_file


@csrf_protect
def Login(request):
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return HttpResponse("您的号被封了, 请联系本站管理员")
        else:
            return HttpResponse("请注册")
    return render(request, 'User/login.html', {'form': form})


def Logout(request):
    logout(request)
    return HttpResponse("注销成功")


@login_required(login_url='/login/')
def index(request):
    email = request.user.email
    return render(request, 'User/index.html', {'email': email})

@login_required(login_url='/login/')
def upload_file(request):
    email = request.user.email
    user_name = request.user.username
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'], user_name)
                return HttpResponse("文件上传成功")
        else:
            form = UploadFileForm()
        return render_to_response('upload.html', {'form': form})

    return render(request, 'User/upload.html', {'email': email, 'form':form})


@login_required(login_url='/login/')
def download_file(request):
    return render(request, 'User/download.html', {})


@login_required(login_url='/login/')
def share_file(request):
    return render(request, 'User/share.html', {})


@login_required(login_url='/login/')
def list_file(request):
    return render(request, 'User/list.html', {})