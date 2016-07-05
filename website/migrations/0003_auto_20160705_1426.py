# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-05 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_recipeingredient_forshopping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(blank=True, choices=[(b'g', b'g'), (b'kg', b'kg'), (b'ml', b'ml'), (None, None), (b'tbsp', b'tbsp')], default=b'kg', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
    ]