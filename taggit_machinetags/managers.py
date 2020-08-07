# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager, _TaggableManager
from taggit.utils import require_instance_manager

from taggit_machinetags.models import MachineTaggedItem


class _MachineTaggableManager(_TaggableManager):

    def _tag_str_to_slug_dict(self, tag_str, include_defaults=True):
        if ':' in tag_str:
            ns, val = tag_str.split(':', 1)
        else:
            ns, val = ('', tag_str)
        slug_dict = dict(namespace_slug=slugify(ns), name_slug=slugify(val))
        if include_defaults:
            slug_dict['defaults'] = {'namespace': ns, 'name': val}
        return slug_dict

    @require_instance_manager
    def add(self, *tags):
        str_tags = set()
        tag_objs = set()
        for t in tags:
            if isinstance(t, self.through.tag_model()):
                if t.pk:
                    tag_objs.add(t)
                else:
                    str_tags.add('{0.namespace}:{0.name}'.format(t))
            elif isinstance(t, str):
                str_tags.add(t)
            else:
                raise ValueError(
                    'Cannot add {0} ({1}). Expected {2} or str.'.format(
                        t, type(t), type(self.through.tag_model())
                    )
                )

        existing = []
        if str_tags:
            q = Q()
            for st in str_tags:
                q.add(Q(**self._tag_str_to_slug_dict(st, False)), Q.OR)
            existing = self.through.tag_model().objects.filter(q)

        tag_objs.update(existing)

        existing_slugs = set(':'.join([t.namespace, t.name])
                             for t in existing)

        for new_tag in str_tags - existing_slugs:
            tag_objs.add(
                self.through.tag_model().objects.get_or_create(
                    **self._tag_str_to_slug_dict(new_tag))[0])

        for tag in tag_objs:
            if not tag.pk:
                tag.save()
            self.through.objects.get_or_create(
                tag=tag, **self._lookup_kwargs())

    @require_instance_manager
    def remove(self, *tags):
        str_tags = set(
            [t for t in tags if not isinstance(t, self.through.tag_model())]
        )
        tag_objs = set(tags) - str_tags

        tags_from_str = []
        if str_tags:
            q = Q()
            for st in str_tags:
                q.add(Q(**self._tag_str_to_slug_dict(st, False)), Q.OR)
            tags_from_str = self.through.tag_model().objects.filter(q)

        tag_objs.update(tags_from_str)

        self.through.objects.filter(
            **self._lookup_kwargs()).filter(tag__in=list(tag_objs)).delete()


class MachineTaggableManager(TaggableManager):

    def __init__(self, **kwargs):
        kwargs.setdefault('through', MachineTaggedItem)
        return super(MachineTaggableManager, self).__init__(**kwargs)

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError(
                '{0} objects need to have a primary key value '
                'before you can access their tags.'
                .format(model.__class__.__name__)
            )
        try:
            manager = _MachineTaggableManager(
                through=self.through, model=model, instance=instance
            )
        except TypeError:
            # django-taggit>0.10
            manager = _MachineTaggableManager(
                through=self.through, model=model, instance=instance,
                prefetch_cache_name=self.name
            )
        return manager
