# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings
import User.models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_auto_20150503_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataOfUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.CharField(max_length=1, choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filefromuser',
            name='date_upload',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 15, 38, 34, 295637, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filefromuser',
            name='file',
            field=models.FileField(upload_to=User.models.upload_file_path),
            preserve_default=True,
        ),
    ]
