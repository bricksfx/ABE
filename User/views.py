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
from .file_handle import handle_uploaded_file, delete_file, make_file_path_for_model, set_tmp_path, set_user_abe_key_path, file_key_encrypt
from .admin import UserCreationForm
from .decrypt import decrypt_file
from .models import *
from encrypt import encrypt_file, create_key
from decrypt import decrypt_file
from django.core.files import File
from django.http import StreamingHttpResponse
from django.http import JsonResponse


def Register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
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
    user = request.user
    academys = Academy.objects.all()
    return render(request, 'User/index.html', {'user': user, 'academys': academys})



@login_required(login_url='/login/')
def upload_file(request):
    user = request.user
    user_name = request.user.username
    academys = Academy.objects.all()
    form = UploadFileFormFromModel()
    if request.method == 'POST':
        form = UploadFileFormFromModel(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'], request.user.username)
            path_of_model = make_file_path_for_model(request.user.username) + request.FILES['file'].name.split("/")[-1]
            key = create_key()
            encrypt_file(key, path, path_of_model)

            try:
                new_model_file = open(path_of_model, 'r')
            except IOError, ex:
                print ex
            if delete_file(path):
                new_file = FileFromUser()
                new_file.user = request.user
                new_file.share = form.cleaned_data['share']
                new_file.share_type = form.cleaned_data['share_type']
                new_file.key = key
                new_file.file = File(new_model_file)
                new_file.save()
                new_model_file.close()
                delete_file(path_of_model)
            else:
                raise Http404
            print new_file.share
            print type(new_file.share)
            file_key_encrypt(request.user.id, new_file.id, new_file.share, new_file.key)
            return HttpResponse("文件上传成功")

        else:
            form = UploadFileForm()
        return render_to_response('User/upload.html', {'form': form})

    return render(request, 'User/upload.html', {'user': user, 'form': form, 'academys': academys})


@login_required(login_url='/login/')
def download_file(request):
    academys = Academy.objects.all()
    user = request.user
    try:
        user_files = FileFromUser.objects.filter(user=user)
    except FileFromUser.DoesNotExist, ex:
        print ex

    return render(request, 'User/download.html', {'user': user, 'user_files': user_files, 'academys': academys})


@login_required(login_url='/login/')
def file_down_single(request, file_id):
    try:
        file = FileFromUser.objects.get(id=file_id)
    except FileFromUser.DoesNotExist, ex:
        return HttpResponse("您所寻找的文件可能已被删除")

    out_path = set_tmp_path(request.user.username) + file.file.path.split("/")[-1]
    decrypt_file(file.key, file.file.path, out_path)

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        delete_file(file_name)
    the_file_name = out_path
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

@login_required(login_url='/login/')
def file_delete(request, file_id):
    try:
        file_delete = FileFromUser.objects.get(id=file_id)
    except FileFromUser.DoesNotExist, ex:
        return HttpResponse("您所要删除的文件不存在")
    file_path = file_delete.file.path
    file_delete.delete()
    delete_file(file_path)
    return HttpResponse("文件删成功")


@login_required(login_url='/login/')
def share_file(request):
    academys = Academy.objects.all()
    user = request.user
    return render(request, 'User/share.html', {'user': user, 'academys': academys})


@login_required(login_url='/login/')
def list_file(request):
    academys = Academy.objects.all()
    user = request.user
    return render(request, 'User/list.html', {'user': user, 'academys': academys})


@login_required(login_url='/login/')
def get_department(request):
    if request.method == 'POST':
        academy = int(request.POST['academy'])
        try:
            departments = Department.objects.filter(academy_id=academy)
        except Department.DoesNotExist, ex:
            print ex
        department_id = []
        department_name = []
        for department in departments:
            department_id.append(department.id)
            department_name.append(department.name)

        department_info = dict(zip(department_id, department_name))
        return JsonResponse(department_info)


def get_department_multiple(request):
    if request.method == 'POST':
        print request.POST
        academy = request.POST['academy']
        academy_single = academy.split(',')
        department_id = []
        department_name = []
        for item in academy_single:
            try:
                departments = Department.objects.filter(academy_id=int(item))
            except Department.DoesNotExist, ex:
                print ex
            for department in departments:
                department_id.append(department.id)
                department_name.append(department.name)

        department_info = dict(zip(department_id, department_name))
        return JsonResponse(department_info)

    return HttpResponse("test")


def data_valid(data):
    errors = 0
    key = []
    value = []
    for item in data:
        if not data[item]:
            errors = 1
            key.append(item)
            value.append('0')
    if errors == 0:
        return {'errors': 0}
    else:
        key.append('errors')
        value.append('1')
        return dict(zip(key, value))


@login_required(login_url='/login/')
def improve_user_info(request):
    if request.method == 'POST':
        data = request.POST
        return_data = data_valid(data)
        if return_data['errors'] == '1':
            return JsonResponse(return_data)
        else:
            try:
                user_info = DataOfUser()
                user_info.user = request.user
                user_info.sex = request.POST['sex']
                print request.POST['sex']
                user_info.academy_id = int(request.POST['academy'])
                user_info.major_id = int(request.POST['department'])
                user_info.identity = request.POST['identity']
                user_info.save()
                set_user_abe_key_path(str(request.user.id))
                import os
                print os.getcwd()
            except Exception, ex:
                return JsonResponse({"errors": "2"})
        return JsonResponse({'errors': '0'})

def upload(request):
    if request.method == 'POST':
        print request.POST
    return render(request, 'User/upload2.html')

def test_upload(request):

    if request.method == 'POST':
        if request.FILES:
            print request.FILES
            print handle_uploaded_file(request.FILES['files[]'], request.user.username)
            return JsonResponse({"test": "test"})
    return render(request, 'User/test_upload.html', {})