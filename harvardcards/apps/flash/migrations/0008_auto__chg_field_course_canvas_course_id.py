# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.canvas_course_id'
        db.alter_column(u'flash_course', 'canvas_course_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Course.canvas_course_id'
        db.alter_column(u'flash_course', 'canvas_course_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flash.analytics': {
            'Meta': {'ordering': "['-stmt_stored', 'stmt_actor_user', 'stmt_actor_desc', 'stmt_verb', 'stmt_object']", 'object_name': 'Analytics'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stmt_actor_desc': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'stmt_actor_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'stmt_context': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stmt_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'stmt_json': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stmt_object': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'stmt_stored': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'stmt_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'stmt_verb': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        u'flash.card': {
            'Meta': {'object_name': 'Card'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '12'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Field']", 'through': u"orm['flash.Cards_Fields']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'flash.cards_fields': {
            'Meta': {'ordering': "['field__sort_order']", 'object_name': 'Cards_Fields'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Card']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'flash.cardtemplate': {
            'Meta': {'object_name': 'CardTemplate'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Field']", 'through': u"orm['flash.CardTemplates_Fields']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'flash.cardtemplates_fields': {
            'Meta': {'ordering': "['field__sort_order']", 'object_name': 'CardTemplates_Fields'},
            'card_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.CardTemplate']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'flash.clone': {
            'Meta': {'ordering': "['-clone_date', 'model', 'model_id', 'cloned_by']", 'object_name': 'Clone'},
            'clone_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cloned_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'model_id': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'flash.cloned': {
            'Meta': {'ordering': "['-clone', 'model', 'old_model_id', 'new_model_id']", 'object_name': 'Cloned'},
            'clone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Clone']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'new_model_id': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'old_model_id': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        u'flash.collection': {
            'Meta': {'object_name': 'Collection'},
            'card_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.CardTemplate']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['flash.Users_Collections']", 'symmetrical': 'False'})
        },
        u'flash.course': {
            'Meta': {'ordering': "['course_id', 'course_name_short', 'course_name']", 'object_name': 'Course'},
            'canvas_course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'course_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'course_id_only': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'course_name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'course_name_short': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'flash.course_map': {
            'Meta': {'ordering': "['course_id', 'collection__id', 'subscribe']", 'object_name': 'Course_Map'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'flash.deck': {
            'Meta': {'ordering': "['sort_order', 'title']", 'object_name': 'Deck'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Card']", 'through': u"orm['flash.Decks_Cards']", 'symmetrical': 'False'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'flash.decks_cards': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Decks_Cards'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Card']"}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Deck']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'flash.field': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Field'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'example_value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'show_label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'flash.mediastore': {
            'Meta': {'ordering': "['file_name']", 'object_name': 'MediaStore'},
            'file_md5hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'file_size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'store_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'store_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'flash.users_collections': {
            'Meta': {'object_name': 'Users_Collections'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['flash']