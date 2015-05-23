#coding=utf8
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,
    )
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True)
    date_of_birth = models.DateField(verbose_name="出生日期")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


def upload_file_path(instance, filename):
    import time
    import os
    path = "file/" + instance.user.username + time.strftime("/%Y/%m/%d/") + filename.split('/')[-1]
    print "model filename", filename
    print "model filepath", path
    print path
    print '/'.join(['content', instance.user.username, filename])
    # return '/'.join(['content', instance.user.username, filename])
    return path


class FileFromUser(models.Model):
    Share_Info = {
        ('1', '公开'),
        ('2', '可共享'),
        ('3', '私人')
    }
    user = models.ForeignKey(MyUser)
    file = models.FileField(upload_to=upload_file_path)
    share = models.CharField(max_length=400)
    key = models.CharField(max_length=200)
    date_upload = models.DateTimeField(auto_now_add=True)
    share_type = models.CharField(max_length=1, choices=Share_Info)

    def __unicode__(self):
        return self.file.name.split('/')[-1]

    def file_size_humanility(self):
        size = self.file.size
        if size <= 1000:
            return str(size) + u"bit"
        elif (size >= 1000) and (size <= 1000000):
            return str(round(size/1000.0, 2)) + u"KB"
        elif (size >= 1000000) and (size <= 1000000000):
            return str(round(size/1000000.0, 2)) + u"MB"
        elif (size >= 1000000000) and (size <= 1000000000000):
            return str(round(size/1000000000.0, 2)) + u"GB"


class Academy(models.Model):

    name = models.CharField(verbose_name="学院名称", max_length=100)

    class Meta:
        verbose_name = "学院"
        verbose_name_plural = "学院"

    def __unicode__(self):
        return self.name

class Department(models.Model):
    academy = models.ForeignKey(Academy)
    name = models.CharField(verbose_name="专业名称", max_length=100)

    class Meta:
        verbose_name = "系"
        verbose_name_plural = "系"

    def __unicode__(self):
        return self.name


class DataOfUser(models.Model):

    SexInfo = {
        ('1', '女'),
        ('2', '男'),
    }
    identityInfo = {
        ('4', '本科生'),
        ('5', '研究生'),
        ('6', '教师')
    }
    user = models.OneToOneField(MyUser)
    sex = models.CharField(verbose_name="性别", max_length=1, choices=SexInfo)
    academy = models.ForeignKey(Academy)
    major = models.ForeignKey(Department, verbose_name="所在系")
    identity = models.CharField(verbose_name="身份", max_length=1, choices=identityInfo)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"


class MessageList(models.Model):
    user = models.ForeignKey(MyUser)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    file_plug_in = models.ForeignKey(FileFromUser, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = "信息列表"
        verbose_name_plural = "信息列表"


class MessageListInline(models.Model):
    messageList = models.ForeignKey(MessageList)
    content = models.CharField(max_length=125)
    user = models.ForeignKey(MyUser)
    user_pre = models.CharField(verbose_name="上一个用户", max_length=30, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username + "->"

    class Meta:
        verbose_name = "回复信息"
        verbose_name_plural = "回复信息"