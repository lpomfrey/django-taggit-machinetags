# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TransactionTestCase
from mock import Mock

from taggit_machinetags.managers import (MachineTaggableManager,
                                         _MachineTaggableManager)
from taggit_machinetags.models import MachineTag


class TestMachineTagModel(TransactionTestCase):

    def test_save_sets_slugs(self):
        tag = MachineTag.objects.create(
            name='Some Name',
            name_slug='',
            namespace='Name Space',
            namespace_slug='',
            slug='',
        )
        self.assertEqual(tag.name_slug, 'some-name')
        self.assertEqual(tag.namespace_slug, 'name-space')
        self.assertEqual(tag.slug, 'name-space:some-name')
        tag.delete()
        tag = MachineTag.objects.create(
            name='Some Name',
            name_slug='n',
            namespace='Name Space',
            namespace_slug='ns',
            slug='ns:slug',
        )
        self.assertEqual(tag.name_slug, 'n')
        self.assertEqual(tag.namespace_slug, 'ns')
        self.assertEqual(tag.slug, 'ns:slug')
        tag.delete()


class TestMachineTaggableManager(TransactionTestCase):

    def test_tag_str_to_slug_dict(self):
        try:
            manager = _MachineTaggableManager(None, None, None)
        except TypeError:
            manager = _MachineTaggableManager(None, None, None, None)
        self.assertEqual(
            manager._tag_str_to_slug_dict('Just a name', False),
            {'namespace_slug': '', 'name_slug': 'just-a-name'}
        )
        self.assertEqual(
            manager._tag_str_to_slug_dict('In a space:Just a name', True),
            {
                'defaults': {
                    'namespace': 'In a space',
                    'name': 'Just a name',
                },
                'namespace_slug': 'in-a-space',
                'name_slug': 'just-a-name',
            }
        )
        self.assertEqual(
            manager._tag_str_to_slug_dict(
                'In a space:Just a name:With a colon', False),
            {
                'namespace_slug': 'in-a-space',
                'name_slug': 'just-a-namewith-a-colon',
            }
        )

    def test_add(self):
        try:
            manager = _MachineTaggableManager(None, None, None)
        except TypeError:
            manager = _MachineTaggableManager(None, None, None, None)
        manager.instance = 1
        manager.through = Mock()
        manager.through.tag_model.return_value = MachineTag
        manager._lookup_kwargs = lambda: {}
        # Test with strings
        manager.through.objects.get_or_create.reset_mock()
        manager.add('Machine:Tag')
        self.assertTrue(
            MachineTag.objects.filter(namespace='Machine', name='Tag').exists()
        )
        self.assertTrue(manager.through.objects.get_or_create.called)
        # Test with unsaved tag objects
        manager.through.objects.get_or_create.reset_mock()
        manager.add(MachineTag(namespace='Unsaved', name='Taggy'))
        self.assertTrue(
            MachineTag.objects.filter(
                namespace='Unsaved', name='Taggy').exists()
        )
        self.assertTrue(manager.through.objects.get_or_create.called)
        # Test with saved tag objects
        manager.through.objects.get_or_create.reset_mock()
        manager.add(MachineTag.objects.create(namespace='Saved', name='Thing'))
        self.assertTrue(
            MachineTag.objects.filter(
                namespace='Saved', name='Thing').exists()
        )
        self.assertTrue(manager.through.objects.get_or_create.called)
        # Test with existing tags
        manager.through.objects.get_or_create.reset_mock()
        manager.add('Unsaved:Taggy')
        self.assertEqual(
            MachineTag.objects.filter(
                namespace='Unsaved', name='Taggy').count(),
            1
        )
        self.assertTrue(manager.through.objects.get_or_create.called)
        # Test multiple
        manager.through.objects.get_or_create.reset_mock()
        manager.add('Unsaved:Taggy', 'Taggy:McTag', 'Some:Property')
        self.assertEqual(manager.through.objects.get_or_create.call_count, 3)

    def test_remove(self):
        tag = MachineTag.objects.create(namespace='NS', name='N')
        tag_2 = MachineTag.objects.create(namespace='NS', name='N2')
        try:
            manager = _MachineTaggableManager(None, None, None)
        except TypeError:
            manager = _MachineTaggableManager(None, None, None, None)
        manager.instance = 1
        manager.through = Mock()
        manager.through.tag_model.return_value = MachineTag
        manager._lookup_kwargs = lambda: {}
        # Test with string
        manager.remove('NS:N')
        manager.through.objects.filter.return_value.filter.assert_called_with(
            tag__in=[tag])
        manager.through.objects.reset_mock()
        # Test with tag
        manager.remove(tag)
        manager.through.objects.filter.return_value.filter.assert_called_with(
            tag__in=[tag])
        manager.through.objects.reset_mock()
        # Test with both
        manager.remove(tag, 'NS:N')
        manager.through.objects.filter.return_value.filter.assert_called_with(
            tag__in=[tag])
        manager.through.objects.reset_mock()
        # Test multiple
        manager.remove('NS:N', 'NS:N2')
        manager.through.objects.filter.return_value.filter.assert_called_with(
            tag__in=[tag, tag_2])
        manager.through.objects.reset_mock()

    def test__get__(self):
        manager = MachineTaggableManager()
        with self.assertRaises(ValueError):
            manager.__get__(Mock(pk=None), Mock())
        m = manager.__get__(Mock(), Mock())
        self.assertTrue(isinstance(m, _MachineTaggableManager))
