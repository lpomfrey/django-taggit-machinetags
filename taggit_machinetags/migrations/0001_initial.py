# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_machinetags.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_slug', models.SlugField(max_length=100, editable=False)),
                ('namespace', models.CharField(
                    default='', max_length=100, blank=True)),
                ('namespace_slug', models.SlugField(default='',
                                                    max_length=100, editable=False, blank=True)),
                ('slug', taggit_machinetags.fields.MachineSlugField(
                    unique=True, max_length=201, editable=False)),
            ],
            options={
                'verbose_name': 'Machine tag',
                'verbose_name_plural': 'Machine tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineTaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(
                    verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='taggit_machinetags_machinetaggeditem_tagged_items',
                                                   verbose_name='Content type', to='contenttypes.ContentType',
                                                   on_delete=models.CASCADE)),
                ('tag', models.ForeignKey(related_name='taggit_machinetags_machinetaggeditem_items',
                                          to='taggit_machinetags.MachineTag', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
