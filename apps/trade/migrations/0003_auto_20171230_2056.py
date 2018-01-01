# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-30 20:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20171228_1837'),
        ('trade', '0002_auto_20171227_0001'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set([('user', 'goods')]),
        ),
    ]
