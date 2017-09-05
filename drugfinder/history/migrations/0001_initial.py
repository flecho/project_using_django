# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 03:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drugs', '0014_auto_20170904_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kor_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.Drug')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together=set([('email', 'kor_name')]),
        ),
    ]