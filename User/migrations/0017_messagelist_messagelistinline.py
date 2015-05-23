# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0016_auto_20150518_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file_plug_in', models.ForeignKey(to='User.FileFromUser', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4fe1\u606f\u5217\u8868',
                'verbose_name_plural': '\u4fe1\u606f\u5217\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageListInline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=125)),
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
