#coding=utf8
from django import forms
from django.forms import ModelForm
from User.models import FileFromUser


class UploadFileForm(forms.Form):

    title = forms.CharField(label="标题", max_length=50)
    file = forms.FileField(label="文件")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()

class UploadFileFormFromModel(ModelForm):
    class Meta:
        model = FileFromUser

