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
            date_of_birth=date_of_birth
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
    path = instance.user.username + time.strftime("/%Y/%m/%d/") + filename
    print path
    print '/'.join(['content', instance.user.username, filename])
    # return '/'.join(['content', instance.user.username, filename])
    return path


class FileFromUser(models.Model):

    user = models.ForeignKey(MyUser)
    file = models.FileField(upload_to=upload_file_path)
    share = models.CharField(max_length=30)
    key = models.CharField(max_length=200)
    date_upload = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, default='1')
    def __unicode__(self):
        return self.user.username


class DataOfUser(models.Model):

    SexInfo = {
        ('F', '女'),
        ('M', '男'),
    }
    user = models.OneToOneField(MyUser)
    sex = models.CharField(max_length=1, choices=SexInfo)

    def __unicode__(self):
        return self.user.username