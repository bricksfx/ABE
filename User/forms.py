from django import forms


class UploadFileForm(forms.Form):

    title = forms.CharField("标题", max_length=50)
    file = forms.FileField("文件")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()

