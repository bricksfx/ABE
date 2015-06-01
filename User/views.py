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
from .file_handle import handle_uploaded_file, delete_file, make_file_path_for_model, set_tmp_path, set_user_abe_key_path, file_key_encrypt, generator_key_for_user, generator_key_for_user_self
from .admin import UserCreationForm
from .decrypt import decrypt_file
from .models import *
from encrypt import encrypt_file, create_key
from decrypt import decrypt_file
from django.core.files import File
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

identityInfo = {u'4': u'本科生', u'5': u'研究生', u'6': u'教师'}
danger_file_suffix = ['.java', '.sh', '.jsp', '.asp', '.sh', '.py' '.php', '.cgi']


@login_required(login_url='/login/')
def user_info_if_complete_authenticate(request):

    if request.method == 'POST':
        try:
            user_info = DataOfUser.objects.get(user=request.user)
        except DataOfUser.DoesNotExist, ex:
            print ex
            return HttpResponse('1')
        return HttpResponse("2")
    return HttpResponse("error")


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
        flag = 1
        try:
            request.GET['next']
        except KeyError:
            flag = 0
        print flag

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if not flag:
                    return HttpResponseRedirect('/index/')
                else:
                    return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponse("您的号被封了, 请联系本站管理员")
        else:
            return HttpResponse("您的用户名和密码不符合")
    return render(request, 'User/login.html', {'form': form})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


@login_required(login_url='/login/')
def index(request):
    print request.session.session_key
    user = request.user
    academys = Academy.objects.all()
    return render(request, 'User/index.html', {'user': user, 'academys': academys})


def add_file_to_message_list(user, file_plugin):
    content = ''
    if file_plugin.share.find(':') != -1:
        attr = file_plugin.share.split(":")
        sex = attr[0]
        academys_row = attr[2]
        department_row = attr[3]
        identitys_row = attr[1]
        academys = []
        departments = []
        identitys = []
        content = u'给 '
        if academys_row.find(','):
            academys.extend(academys_row.split(','))
        else:
            academys.append(academys_row)

        if department_row.find(','):
            departments.extend(department_row.split(','))
        else:
            departments.append(department_row)
        try:
            for item in academys:
                academy = Academy.objects.get(id=int(item))
                content += (academy.name + ',')
        except Academy.DoesNotExist, ex:
            print ex
        try:
            for item in departments:
                department = Department.objects.get(id=int(item))
                content += (department.name + u'专业,')
        except Department.DoesNotExist, ex:
            print ex
        content += u" 的"
        if identitys_row.find(','):
            identitys.extend(identitys_row.split(','))
        else:
            identitys.append(identitys_row)
        try:
            for item in identitys:
                identity = identityInfo[item]
                content += (identity + u',')
        except KeyError, ex:
            print ex
        content += u'分享了文件.'
        if attr[0] != '0':
            content += u'备注：'
            if attr[0] == '1':
                content += u'只有女生可以下载'
            elif attr[0] == '2':
                content += u'只有男生可以下载'

    if file_plugin.share == 'public':
        content = u'分享了共享文件给所有人'
    message = MessageList()
    message.user = user
    message.content = content
    message.file_plug_in = file_plugin
    message.save()


def time_out_valid(user):
    import datetime
    from django.utils import timezone
    try:
        post_time = PostMessageTimeCheck.objects.get(user=user)
    except PostMessageTimeCheck.DoesNotExist, ex:
        new_post_time_set = PostMessageTimeCheck()
        new_post_time_set.user = user
        new_post_time_set.time = timezone.now()
        new_post_time_set.save()
        return 1
    time_now = timezone.now()
    time_del = (time_now - post_time.time).total_seconds()
    print time_del
    if time_del > 10:
        post_time.time = timezone.now()
        post_time.save()
        return 1
    else:
        post_time.time = timezone.now()
        post_time.save()
        return 0


@login_required(login_url='/login/')
def upload_file(request):
    user = request.user
    user_name = request.user.username
    academys = Academy.objects.all()
    form = UploadFileFormFromModel()
    if request.method == 'POST':
        if not time_out_valid(request.user):
            request.user.is_active = False
            request.user.save()
            logout(request)
            return HttpResponse("您的行为疑似机器登录上传，暂时将您封号，请联系本站管理员")
        try:
            info = DataOfUser.objects.get(user=request.user)
        except DataOfUser.DoesNotExist, ex:
            print ex
            return HttpResponse("请完善用户信息")
        form = UploadFileFormFromModel(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['share_type'] == '2':
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
                file_key_encrypt(request.user, new_file.id, new_file.share, new_file.key, 2)
                add_file_to_message_list(request.user, new_file)

            elif form.cleaned_data['share_type'] == '1':
                file_name = request.FILES['file'].name.split("/")[-1].lower()
                for item in danger_file_suffix:
                    if file_name.endswith(item):
                        return HttpResponse("文件名为可执行文件，可能威胁到服务器，请转为可共享文件分享")
                new_file = FileFromUser()
                new_file.user = request.user
                new_file.share = form.cleaned_data['share']
                new_file.share_type = form.cleaned_data['share_type']
                new_file.key = "public"
                new_file.file = request.FILES['file']
                new_file.save()
                add_file_to_message_list(request.user, new_file)
            else:
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
                file_key_encrypt(request.user, new_file.id, new_file.share, new_file.key, 3)

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
    if file.share_type != '1':
        if (file.share_type == '2' and request.user == file.user) or \
                (file.share_type == '3' and request.user == file.user):
            key = generator_key_for_user_self(request.user, file.id)
        else:
            try:
                key = generator_key_for_user(request.user, file.user.id, file.id)
            except Exception, ex:
                print ex
                return HttpResponse("文件下载出现问题，可能您的属性并不在文件分享对象之内")
        out_path = set_tmp_path(request.user.username) + file.file.path.split("/")[-1]
        decrypt_file(key, file.file.path, out_path)

    def file_iterator(file_name, chunk_size=512, type='1'):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        if type != '1':
            delete_file(file_name)
    if file.share_type == '2' or file.share_type == '3':
        the_file_name = out_path
        response = StreamingHttpResponse(file_iterator(the_file_name, type='2'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name.split("/")[-1].encode('utf-8'))
        return response
    elif file.share_type == '1':
        the_file_name = file.file.path
        response = StreamingHttpResponse(file_iterator(the_file_name, type='1'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name.split("/")[-1].encode('utf-8'))
        return response


@login_required(login_url='/login/')
def file_delete(request, file_id):
    try:
        file_delete_single = FileFromUser.objects.get(id=int(file_id))
    except FileFromUser.DoesNotExist, ex:
        return HttpResponse("您所要删除的文件不存在")
    if file_delete_single.user == request.user:
        file_path = file_delete_single.file.path
        file_delete_single.delete()
        delete_file(file_path)
    else:
        request.user.is_active = False
        request.user.save()
        logout(request)
        return HttpResponse("流氓行为，请不要删除别人的文件,您的号已被封杀")
    return HttpResponse("文件删除成功")


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
        user_info_is_exist = DataOfUser.objects.filter(user=request.user)
        if user_info_is_exist:
            return JsonResponse({"errors": "3"})
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


@login_required(login_url='/login/')
def delete_message(request):
    if request.method == 'POST':
        info = request.POST['info'].split(' ')
        if info[0] == 'btnTop':
            try:
                message = MessageList.objects.get(id=int(info[1]))
            except MessageList.DoesNotExist:
                return HttpResponse("0")
            if request.user == message.user:
                message.delete()
                return HttpResponse("1")
            else:
                return HttpResponse("您尝试删除不属于您的文件，现在已经封了您的号")
        elif info[0] == 'btnInline':
            try:
                message = MessageListInline.objects.get(id=int(info[1]))
            except MessageListInline.DoesNotExist:
                return HttpResponse("0")
            if request.user == message.user:
                return HttpResponse("2")
            else:
                return HttpResponse("您尝试删除不属于您发布的信息，现已经封了您的号")
        else:
            return HttpResponse("你提交的数据格式不正确")

    return HttpResponse("test")


@login_required(login_url='/login/')
def message_list(request):
    messagelist = MessageList.objects.all()
    paginator = Paginator(messagelist, 5)
    page = request.GET.get('page')
    page_num = range(1, paginator.num_pages + 1)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger, ex:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    print messages.has_previous()

    academys = Academy.objects.all()
    user = request.user
    return render(request, 'User/message_list.html', {'user': user, 'academys': academys,
                                                      'messages': messages, 'page_num': page_num})


@login_required(login_url='/login/')
def upload_new_message(request):

    if request.method == 'POST':
        if not time_out_valid(request.user):
            request.user.is_active = False
            request.user.save()
            logout(request)
            return HttpResponse("robot")
        if request.POST['content'] == '':
            return HttpResponse("0")
        try:
            new_message = MessageList()
            new_message.user = request.user
            new_message.content = request.POST['content']
            new_message.save()
        except Exception, ex:
            print ex
            return HttpResponse("1")

        return render(request, 'User/message_single.html', {'message': new_message})
    return HttpResponse("upload new message")


@login_required(login_url='/login/')
def upload_new_inline_message(request):

    if request.method == 'POST':
        if not time_out_valid(request.user):
            request.user.is_active = False
            request.user.save()
            logout(request)
            return HttpResponse("robot")
        user_info = request.POST['info'].split(' ')
        content = request.POST['content']
        print user_info
        try:
            message = MessageList.objects.get(id=int(user_info[1]))
        except MessageList.DoesNotExist, ex:
            print ex
            return HttpResponse('1')
        inline = MessageListInline()
        inline.user = request.user
        inline.content = content
        inline.messageList = message
        if user_info[0] != 'btnTop' and request.user.username != user_info[2]:
            inline.user_pre = user_info[2]
        try:
            inline.save()
        except Exception, ex:
            print ex
            return HttpResponse("2")
        return render(request, 'User/message_inline_single.html', {'message_inline': inline})
    return HttpResponse("upload_new_message_inline")

#TODO phonegap