# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-04 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='forShopping',
            field=models.BooleanField(default=True),
        ),
    ]
