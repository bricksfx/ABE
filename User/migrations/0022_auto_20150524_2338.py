# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0021_auto_20150524_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagelistinline',
            options={'ordering': ['-date'], 'verbose_name': '\u56de\u590d\u4fe1\u606f', 'verbose_name_plural': '\u56de\u590d\u4fe1\u606f'},
        ),
    ]
