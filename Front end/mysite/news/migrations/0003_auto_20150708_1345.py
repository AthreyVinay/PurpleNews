# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article_tweet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='article_id',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
    ]
