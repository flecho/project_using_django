# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0013_auto_20170830_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drug',
            name='id',
        ),
        migrations.AlterField(
            model_name='drug',
            name='kor_name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]