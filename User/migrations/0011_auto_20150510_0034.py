# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_auto_20150508_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataofuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='DataOfUser',
        ),
    ]
