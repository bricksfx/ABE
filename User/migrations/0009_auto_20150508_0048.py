# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_filefromuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filefromuser',
            name='type',
            field=models.CharField(default=b'1', max_length=1),
            preserve_default=True,
        ),
    ]
