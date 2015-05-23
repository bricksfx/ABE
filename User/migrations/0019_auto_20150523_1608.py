# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0018_auto_20150522_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagelistinline',
            name='messageList',
        ),
        migrations.RemoveField(
            model_name='messagelistinline',
            name='user',
        ),
        migrations.DeleteModel(
            name='MessageListInline',
        ),
    ]
