# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_auto_20150515_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataofuser',
            name='identity',
            field=models.CharField(max_length=1, verbose_name=b'\xe8\xba\xab\xe4\xbb\xbd', choices=[(b'4', b'\xe6\x9c\xac\xe7\xa7\x91\xe7\x94\x9f'), (b'6', b'\xe6\x95\x99\xe5\xb8\x88'), (b'5', b'\xe7\xa0\x94\xe7\xa9\xb6\xe7\x94\x9f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filefromuser',
            name='share',
            field=models.CharField(max_length=400),
            preserve_default=True,
        ),
    ]
