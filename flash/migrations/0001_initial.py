# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Field'
        db.create_table(u'flash_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('show_label', self.gf('django.db.models.fields.BooleanField')()),
            ('display', self.gf('django.db.models.fields.BooleanField')()),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('example_value', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'flash', ['Field'])

        # Adding model 'CardTemplate'
        db.create_table(u'flash_cardtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'flash', ['CardTemplate'])

        # Adding model 'Collection'
        db.create_table(u'flash_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('card_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.CardTemplate'])),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'flash', ['Collection'])

        # Adding model 'Card'
        db.create_table(u'flash_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Collection'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('color', self.gf('django.db.models.fields.CharField')(default='default', max_length=12)),
        ))
        db.send_create_signal(u'flash', ['Card'])

        # Adding model 'Deck'
        db.create_table(u'flash_deck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Collection'])),
        ))
        db.send_create_signal(u'flash', ['Deck'])

        # Adding model 'Decks_Cards'
        db.create_table(u'flash_decks_cards', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Deck'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Card'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'flash', ['Decks_Cards'])

        # Adding model 'Cards_Fields'
        db.create_table(u'flash_cards_fields', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Card'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Field'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'flash', ['Cards_Fields'])

        # Adding model 'CardTemplates_Fields'
        db.create_table(u'flash_cardtemplates_fields', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.CardTemplate'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Field'])),
        ))
        db.send_create_signal(u'flash', ['CardTemplates_Fields'])

        # Adding model 'Users_Collections'
        db.create_table(u'flash_users_collections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Collection'])),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
            ('role', self.gf('django.db.models.fields.CharField')(default='O', max_length=1)),
        ))
        db.send_create_signal(u'flash', ['Users_Collections'])

        # Adding model 'Canvas_Course_Map'
        db.create_table(u'flash_canvas_course_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('canvas_course_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.Collection'])),
            ('subscribe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'flash', ['Canvas_Course_Map'])


    def backwards(self, orm):
        # Deleting model 'Field'
        db.delete_table(u'flash_field')

        # Deleting model 'CardTemplate'
        db.delete_table(u'flash_cardtemplate')

        # Deleting model 'Collection'
        db.delete_table(u'flash_collection')

        # Deleting model 'Card'
        db.delete_table(u'flash_card')

        # Deleting model 'Deck'
        db.delete_table(u'flash_deck')

        # Deleting model 'Decks_Cards'
        db.delete_table(u'flash_decks_cards')

        # Deleting model 'Cards_Fields'
        db.delete_table(u'flash_cards_fields')

        # Deleting model 'CardTemplates_Fields'
        db.delete_table(u'flash_cardtemplates_fields')

        # Deleting model 'Users_Collections'
        db.delete_table(u'flash_users_collections')

        # Deleting model 'Canvas_Course_Map'
        db.delete_table(u'flash_canvas_course_map')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flash.canvas_course_map': {
            'Meta': {'ordering': "['canvas_course_id', 'collection__id', 'subscribe']", 'object_name': 'Canvas_Course_Map'},
            'canvas_course_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'flash.card': {
            'Meta': {'object_name': 'Card'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '12'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Field']", 'through': u"orm['flash.Cards_Fields']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'flash.cardtemplates_fields': {
            'Meta': {'ordering': "['field__sort_order']", 'object_name': 'CardTemplates_Fields'},
            'card_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.CardTemplate']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'flash.deck': {
            'Meta': {'object_name': 'Deck'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Card']", 'through': u"orm['flash.Decks_Cards']", 'symmetrical': 'False'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Collection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'flash.decks_cards': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Decks_Cards'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Card']"}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.Deck']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'flash.field': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Field'},
            'display': ('django.db.models.fields.BooleanField', [], {}),
            'example_value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'show_label': ('django.db.models.fields.BooleanField', [], {}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
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