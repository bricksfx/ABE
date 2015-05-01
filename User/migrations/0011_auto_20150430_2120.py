# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_filefromuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filefromuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='FileFromUser',
        ),
    ]
