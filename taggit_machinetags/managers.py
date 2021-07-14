# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import router
from django.db.models import Q, signals
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager, _TaggableManager
from taggit.utils import require_instance_manager

from taggit_machinetags.models import MachineTaggedItem


class _MachineTaggableManager(_TaggableManager):
    def _tag_str_to_slug_dict(self, tag_str, include_defaults=True):
        if ":" in tag_str:
            ns, val = tag_str.split(":", 1)
        else:
            ns, val = ("", tag_str)
        slug_dict = dict(namespace_slug=slugify(ns), name_slug=slugify(val))

        if include_defaults:
            slug_dict["defaults"] = {"namespace": ns, "name": val}

        return slug_dict

    def _to_tag_model_instances(self, tags, tag_kwargs=None):
        if tag_kwargs is None:
            tag_kwargs = {}

        db = router.db_for_write(self.through, instance=self.instance)

        str_tags = set()
        tag_objs = set()

        for t in tags:
            if isinstance(t, self.through.tag_model()):
                if t.pk:
                    tag_objs.add(t)
                else:
                    str_tags.add("{0.namespace}:{0.name}".format(t))
            elif isinstance(t, str):
                str_tags.add(t)
            else:
                raise ValueError(
                    "Cannot add {0} ({1}). Expected {2} or str.".format(
                        t, type(t), type(self.through.tag_model())
                    )
                )

        manager = self.through.tag_model()._default_manager.using(db)
        existing = []

        if str_tags:
            q = Q()

            for st in str_tags:
                q.add(Q(**self._tag_str_to_slug_dict(st, False)), Q.OR)
            existing = manager.filter(q)

        tag_objs.update(existing)

        existing_slugs = set(":".join([t.namespace, t.name]) for t in existing)

        for new_tag in str_tags - existing_slugs:
            tag_objs.add(
                manager.get_or_create(**self._tag_str_to_slug_dict(new_tag))[0]
            )

        for tag in tag_objs:
            if not tag.pk:
                tag.save()

        return tag_objs

    @require_instance_manager
    def remove(self, *tags):
        if not tags:
            return

        db = router.db_for_write(self.through, instance=self.instance)

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

        qs = (
            self.through._default_manager.using(db)
            .filter(**self._lookup_kwargs())
            .filter(tag__in=tag_objs)
        )

        old_ids = set(qs.values_list("tag_id", flat=True))

        signals.m2m_changed.send(
            sender=self.through,
            action="pre_remove",
            instance=self.instance,
            reverse=False,
            model=self.through.tag_model(),
            pk_set=old_ids,
            using=db,
        )
        qs.delete()
        signals.m2m_changed.send(
            sender=self.through,
            action="post_remove",
            instance=self.instance,
            reverse=False,
            model=self.through.tag_model(),
            pk_set=old_ids,
            using=db,
        )


class MachineTaggableManager(TaggableManager):
    def __init__(self, **kwargs):
        kwargs.setdefault("through", MachineTaggedItem)

        return super(MachineTaggableManager, self).__init__(**kwargs)

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError(
                "{0} objects need to have a primary key value "
                "before you can access their tags.".format(model.__class__.__name__)
            )

        return _MachineTaggableManager(
            through=self.through,
            model=model,
            instance=instance,
            prefetch_cache_name=self.name,
        )
