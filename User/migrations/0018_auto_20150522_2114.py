# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_messagelist_messagelistinline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagelist',
            name='file_plug_in',
            field=models.ForeignKey(blank=True, to='User.FileFromUser', null=True),
            preserve_default=True,
        ),
    ]
