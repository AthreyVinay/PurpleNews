# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20150709_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
    ]
