# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0012_auto_20150510_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataofuser',
            name='identity',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'3', b'\xe6\x95\x99\xe5\xb8\x88'), (b'2', b'\xe7\xa0\x94\xe7\xa9\xb6\xe7\x94\x9f'), (b'1', b'\xe5\xad\xa6\xe7\x94\x9f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataofuser',
            name='sex',
            field=models.CharField(default=b'1', max_length=1, choices=[(b'2', b'\xe7\x94\xb7'), (b'1', b'\xe5\xa5\xb3')]),
            preserve_default=True,
        ),
    ]
