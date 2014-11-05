# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MachineTag'
        db.create_table(u'taggit_machinetags_machinetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=u'', max_length=100, blank=True)),
            ('namespace_slug', self.gf('django.db.models.fields.SlugField')(default=u'', max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=201)),
        ))
        db.send_create_signal(u'taggit_machinetags', ['MachineTag'])

        # Adding model 'MachineTaggedItem'
        db.create_table(u'taggit_machinetags_machinetaggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'taggit_machinetags_machinetaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'taggit_machinetags_machinetaggeditem_items', to=orm['taggit_machinetags.MachineTag'])),
        ))
        db.send_create_signal(u'taggit_machinetags', ['MachineTaggedItem'])


    def backwards(self, orm):
        # Deleting model 'MachineTag'
        db.delete_table(u'taggit_machinetags_machinetag')

        # Deleting model 'MachineTaggedItem'
        db.delete_table(u'taggit_machinetags_machinetaggeditem')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit_machinetags.machinetag': {
            'Meta': {'object_name': 'MachineTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'namespace_slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '201'})
        },
        u'taggit_machinetags.machinetaggeditem': {
            'Meta': {'object_name': 'MachineTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_machinetags_machinetaggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_machinetags_machinetaggeditem_items'", 'to': u"orm['taggit_machinetags.MachineTag']"})
        }
    }

    complete_apps = ['taggit_machinetags']