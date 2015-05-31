#coding=utf8
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin import widgets

from User.models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    date_of_birth = forms.DateField(label="出生日期", widget=widgets.AdminDateWidget)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('email', 'email', 'username', 'date_of_birth',)
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'date_of_birth', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('is_active', {'fields': ('is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


class AcademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class FileFromUserAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'file', 'date_upload', 'share_type', 'share_type', 'share', 'key')
    list_display = ('id', 'user', 'file', 'date_upload', 'share_type', 'share_type')

class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'academy', 'name',)

class MessageListAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'content', 'file_plug_in', 'date')
    list_display = ('id', 'user', 'content', 'file_plug_in', 'date')

class DateOfUserAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'sex', 'academy', 'major', 'identity')
    list_display = ('id', 'user', 'academy', 'major', 'identity')

class MessageListInlineAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'messageList', 'content', 'user', 'user_pre')
    list_display = ('id', 'messageList', 'content', 'user', 'user_pre')

# Now register the new UserAdmin...
admin.site.register(MyUser, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
admin.site.register(FileFromUser, FileFromUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Academy, AcademyAdmin)
admin.site.register(DataOfUser, DateOfUserAdmin)
admin.site.register(MessageList, MessageListAdmin)
admin.site.register(MessageListInline, MessageListInlineAdmin)



