# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TransactionTestCase

from taggit_machinetags.models import MachineTag

from test_project.test_app.models import TestModel


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
        tm = TestModel()
        tm.save()
        manager = tm.tags
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
        tm = TestModel()
        tm.save()
        manager = tm.tags
        # Test with strings
        manager.clear()
        manager.add('Machine:Tag')
        self.assertTrue(
            MachineTag.objects.filter(namespace='Machine', name='Tag').exists()
        )
        self.assertEqual(manager.count(), 1)
        # Test with unsaved tag objects
        manager.clear()
        manager.add(MachineTag(namespace='Unsaved', name='Taggy'))
        self.assertTrue(
            MachineTag.objects.filter(
                namespace='Unsaved', name='Taggy').exists()
        )
        self.assertEqual(manager.count(), 1)
        # Test with saved tag objects
        manager.clear()
        manager.add(MachineTag.objects.create(namespace='Saved', name='Thing'))
        self.assertTrue(
            MachineTag.objects.filter(
                namespace='Saved', name='Thing').exists()
        )
        self.assertEqual(manager.count(), 1)
        # Test with existing tags
        manager.clear()
        manager.add('Unsaved:Taggy')
        self.assertEqual(
            MachineTag.objects.filter(
                namespace='Unsaved', name='Taggy').count(),
            1
        )
        self.assertTrue(manager.count() == 1)
        # Test multiple
        manager.clear()
        manager.add('Unsaved:Taggy', 'Taggy:McTag', 'Some:Property')
        self.assertEqual(manager.count(), 3)

    def test_remove(self):
        tag = MachineTag.objects.create(namespace='NS', name='N')
        tag_2 = MachineTag.objects.create(namespace='NS', name='N2')
        tm = TestModel()
        tm.save()
        manager = tm.tags
        manager.set(tag, tag_2)
        self.assertEqual(manager.count(), 2)
        # Test with string
        manager.remove('NS:N')
        self.assertEqual(manager.count(), 1)
        # Test with tag
        manager.set(tag, tag_2)
        manager.remove(tag)
        self.assertEqual(manager.count(), 1)
        # Test with both forms of same tag
        manager.set(tag, tag_2)
        manager.remove(tag, 'NS:N')
        self.assertEqual(manager.count(), 1)
        # Test multiple slugs
        manager.set(tag, tag_2)
        manager.remove('ns:n', 'ns:n2')
        self.assertEqual(manager.count(), 0)
