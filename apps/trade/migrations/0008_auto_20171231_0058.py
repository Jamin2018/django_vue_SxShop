# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 00:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_auto_20171231_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='trade.OrderInfo', verbose_name='订单信息'),
        ),
    ]
