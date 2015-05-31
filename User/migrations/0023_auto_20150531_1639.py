# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0022_auto_20150524_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostMessageTimeCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u673a\u5668\u8bc4\u8bba\u63d0\u4ea4\u5ba1\u6838',
                'verbose_name_plural': '\u7528\u6237\u673a\u5668\u8bc4\u8bba\u63d0\u4ea4\u5ba1\u6838',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='filefromuser',
            options={'verbose_name': '\u6587\u4ef6', 'verbose_name_plural': '\u6587\u4ef6'},
        ),
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': '\u7528\u6237', 'verbose_name_plural': '\u7528\u6237'},
        ),
    ]
