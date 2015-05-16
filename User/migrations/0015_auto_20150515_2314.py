# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_auto_20150510_0114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academy',
            options={'verbose_name': '\u5b66\u9662', 'verbose_name_plural': '\u5b66\u9662'},
        ),
        migrations.AlterModelOptions(
            name='dataofuser',
            options={'verbose_name': '\u7528\u6237\u4fe1\u606f', 'verbose_name_plural': '\u7528\u6237\u4fe1\u606f'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '\u7cfb', 'verbose_name_plural': '\u7cfb'},
        ),
        migrations.AlterField(
            model_name='dataofuser',
            name='identity',
            field=models.CharField(max_length=1, verbose_name=b'\xe8\xba\xab\xe4\xbb\xbd', choices=[(b'3', b'\xe6\x95\x99\xe5\xb8\x88'), (b'2', b'\xe7\xa0\x94\xe7\xa9\xb6\xe7\x94\x9f'), (b'1', b'\xe6\x9c\xac\xe7\xa7\x91\xe7\x94\x9f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataofuser',
            name='major',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\x9c\xa8\xe7\xb3\xbb', to='User.Department'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataofuser',
            name='sex',
            field=models.CharField(max_length=1, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(b'2', b'\xe7\x94\xb7'), (b'1', b'\xe5\xa5\xb3')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filefromuser',
            name='share_type',
            field=models.CharField(max_length=1, choices=[(b'3', b'\xe7\xa7\x81\xe4\xba\xba'), (b'1', b'\xe5\x85\xac\xe5\xbc\x80'), (b'2', b'\xe5\x8f\xaf\xe5\x85\xb1\xe4\xba\xab')]),
            preserve_default=True,
        ),
    ]
