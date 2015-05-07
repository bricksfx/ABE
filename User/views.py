#coding=utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect
from .forms import UploadFileForm, LoginForm, UploadFileFormFromModel
from .file_handle import handle_uploaded_file, delete_file, make_file_path_for_model
from .admin import UserCreationForm
from .decrypt import decrypt_file
from .models import *
from encrypt import encrypt_file
from decrypt import decrypt_file
from django.core.files import File


def Register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'User/register.html', {'form': form})

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
    form = UploadFileFormFromModel()
    if request.method == 'POST':
        form = UploadFileFormFromModel(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'], request.user.username)
            path_of_model = make_file_path_for_model(request.user.username)
            encrypt_file(form.cleaned_data['key'], path, path_of_model)

            if delete_file(path):
                print "文件删除成功"
            new_file = FileFromUser()
            new_file.user = request.user
            new_file.share = form.cleaned_data['share']
            new_file.key = ''
            new_file.save()
            print new_file.file.path
            return HttpResponse("文件上传成功")
        else:
            form = UploadFileForm()
        return render_to_response('User/upload.html', {'form': form})

    return render(request, 'User/upload.html', {'email': email, 'form': form})


@login_required(login_url='/login/')
def download_file(request):
    email = request.user.email
    return render(request, 'User/download.html', {'email': email})


@login_required(login_url='/login/')
def share_file(request):
    email = request.user.email
    return render(request, 'User/share.html', {'email': email})


@login_required(login_url='/login/')
def list_file(request):
    email = request.user.email
    return render(request, 'User/list.html', {'email': email})

def upload(request):
    if request.method == 'POST':
        print request.POST
    return render(request, 'User/upload2.html')


def test_upload(request):
    from django.http import JsonResponse

    if request.method == 'POST':
        if request.FILES:
            print request.FILES
            print handle_uploaded_file(request.FILES['files[]'], request.user.username)
            return JsonResponse({"test": "test"})
    return render(request, 'User/test_upload.html', {})