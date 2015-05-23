# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0019_auto_20150523_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageListInline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=125)),
                ('user_pre', models.CharField(max_length=30, null=True, verbose_name=b'\xe4\xb8\x8a\xe4\xb8\x80\xe4\xb8\xaa\xe7\x94\xa8\xe6\x88\xb7', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('messageList', models.ForeignKey(to='User.MessageList')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u56de\u590d\u4fe1\u606f',
                'verbose_name_plural': '\u56de\u590d\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
    ]
