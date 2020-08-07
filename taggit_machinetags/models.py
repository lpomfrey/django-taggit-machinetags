# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from taggit.models import GenericTaggedItemBase

from taggit_machinetags.fields import MachineSlugField


class MachineTagBase(models.Model):

    name = models.CharField(max_length=100)
    name_slug = models.SlugField(max_length=100, editable=False)
    namespace = models.CharField(max_length=100, blank=True, default='')
    namespace_slug = models.SlugField(
        max_length=100, blank=True, default='', editable=False)
    slug = MachineSlugField(
        max_length=201, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = (
            ('namespace', 'name'),
            ('namespace_slug', 'name_slug'),
        )
        abstract = True

    def __str__(self):
        return '{0.namespace}:{0.name}'.format(self)

    def __repr__(self):
        return '<{0.__class__.__name__}: {0.namespace}.{0.name}>'.format(self)

    def save(self, *args, **kwargs):
        if not self.name_slug:
            self.name_slug = slugify(self.name)
        if not self.namespace_slug:
            self.namespace_slug = slugify(self.namespace)
        if not self.slug:
            self.slug = ':'.join([self.namespace_slug, self.name_slug])
        return super(MachineTagBase, self).save(*args, **kwargs)


class MachineTag(MachineTagBase):

    class Meta:
        verbose_name = 'Machine tag'
        verbose_name_plural = 'Machine tags'


class MachineTaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(
        'MachineTag',
        related_name='%(app_label)s_%(class)s_items',
        on_delete=models.CASCADE
    )
