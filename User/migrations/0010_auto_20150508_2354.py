# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_auto_20150508_0048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filefromuser',
            old_name='type',
            new_name='share_type',
        ),
    ]
