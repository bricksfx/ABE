# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20150507_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='filefromuser',
            name='type',
            field=models.CharField(default=1, max_length=1),
            preserve_default=True,
        ),
    ]
