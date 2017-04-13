# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='interview',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='question_app.Interview', verbose_name='Опрос'),
        ),
        migrations.AlterField(
            model_name='votesresult',
            name='interview',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question_app.Interview'),
        ),
    ]