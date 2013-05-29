# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MachineTag'
        db.create_table('machinetags_machinetag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=u'', max_length=100, blank=True)),
            ('namespace_slug', self.gf('django.db.models.fields.SlugField')(default=u'', max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=201)),
        ))
        db.send_create_signal('machinetags', ['MachineTag'])

        # Adding unique constraint on 'MachineTag', fields ['namespace', 'name']
        db.create_unique('machinetags_machinetag', ['namespace', 'name'])

        # Adding unique constraint on 'MachineTag', fields ['namespace_slug', 'name_slug']
        db.create_unique('machinetags_machinetag', ['namespace_slug', 'name_slug'])

        # Adding model 'MachineTaggedItem'
        db.create_table('machinetags_machinetaggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='machinetags_machinetaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'machinetags_machinetaggeditem_items', to=orm['machinetags.MachineTag'])),
        ))
        db.send_create_signal('machinetags', ['MachineTaggedItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'MachineTag', fields ['namespace_slug', 'name_slug']
        db.delete_unique('machinetags_machinetag', ['namespace_slug', 'name_slug'])

        # Removing unique constraint on 'MachineTag', fields ['namespace', 'name']
        db.delete_unique('machinetags_machinetag', ['namespace', 'name'])

        # Deleting model 'MachineTag'
        db.delete_table('machinetags_machinetag')

        # Deleting model 'MachineTaggedItem'
        db.delete_table('machinetags_machinetaggeditem')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'machinetags.machinetag': {
            'Meta': {'unique_together': "((u'namespace', u'name'), (u'namespace_slug', u'name_slug'))", 'object_name': 'MachineTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'namespace_slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '201'})
        },
        'machinetags.machinetaggeditem': {
            'Meta': {'object_name': 'MachineTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'machinetags_machinetaggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'machinetags_machinetaggeditem_items'", 'to': "orm['machinetags.MachineTag']"})
        }
    }

    complete_apps = ['machinetags']