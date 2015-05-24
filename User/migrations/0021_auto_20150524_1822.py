# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0020_messagelistinline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagelist',
            options={'ordering': ['-date'], 'verbose_name': '\u4fe1\u606f\u5217\u8868', 'verbose_name_plural': '\u4fe1\u606f\u5217\u8868'},
        ),
    ]
