# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='country',
            field=models.CharField(max_length=20),
        ),
    ]
