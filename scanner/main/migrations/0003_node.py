# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-07 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151230_0344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sha1_id', models.CharField(max_length=40)),
                ('hotkey_info', models.CommaSeparatedIntegerField(max_length=200)),
            ],
        ),
    ]
