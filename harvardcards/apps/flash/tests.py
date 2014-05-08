from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.test.client import RequestFactory, Client

from harvardcards.apps.flash.models import Collection, Deck, Field, CardTemplate, CardTemplates_Fields, Card
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash.views.collection import *
from harvardcards.apps.flash import services, queries

import unittest

class CollectionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #TODO why is this failing?
	    #This test isn't failing

        #self.assertTemplateUsed(response, 'index.html')

    def test_collection_get(self):
        url = reverse('collectionIndex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_collection_create(self):
        url = reverse('collectionCreate')
        post_data = {'title':'foobar', 'card_template':'1'}

        len_collections_before = len(Collection.objects.filter(title__exact=post_data['title']))
        response = self.client.post(url, post_data)
        len_collections_after = len(Collection.objects.filter(title__exact=post_data['title']))

        self.assertEqual(len_collections_before + 1, len_collections_after)

    def test_collection_form(self):
        post_data = {'title':'foobar', 'card_template':'1'}
        form = CollectionForm(post_data)
        self.assertEqual(form.is_valid(), True)
        form1 = CollectionForm({})
        self.assertEqual(form1.is_valid(), False)

class ServicesTest(TestCase):
    def setUp(self):
        """ Every test needs access to the request factory. """
        self.factory = RequestFactory()
        self.client = Client()
        self.card_template = CardTemplate.objects.get(pk=1)

    def makeCollection(self):
        card_template = CardTemplate.objects.create(title='b', description='bbb')
        collection = Collection.objects.create(title='a', description='aaa', card_template=card_template)
        return collection

    def test_deleteCollection(self):
        collection = self.makeCollection()
        self.assertEqual(services.delete_collection(collection.id), True)

    def test_deleteDeck(self):
        collection = self.makeCollection()
        deck = Deck.objects.create(title='a', collection=collection)
        self.assertEqual(services.delete_deck(deck.id), True)

    def test_deleteCard(self):
        collection = self.makeCollection()
        card = Card.objects.create(collection=collection, sort_order=1)
        self.assertEqual(services.delete_card(card.id), True)

class QueriesTest(TestCase):
    def setUp(self):
        """ Every test needs access to the request factory. """
        self.factory = RequestFactory()
        self.client = Client()
        self.card_template = CardTemplate.objects.get(pk=1)

    def test_getCollection(self):
        collection = Collection.objects.create(title='getCollectionTest', description='asdfasdfasdf', card_template=self.card_template)
        gottenCollection = queries.getCollection(collection.id)
        self.assertEqual(gottenCollection.title, 'getCollectionTest')

    def test_getDecksByCollection(self):
        collection = Collection.objects.create(title='a', description='aaa', card_template=self.card_template)
        deck1 = Deck.objects.create(title='d1', collection=collection)
        deck2 = Deck.objects.create(title='d2', collection=collection)
        decksByCollection = queries.getDecksByCollection()
        self.assertEqual(2, len(decksByCollection[collection.id]))
        
    def test_getFieldList(self):
        card_template = CardTemplate.objects.create(title='b', description='bbb')
        collection = Collection.objects.create(title='a', description='aaa', card_template=card_template)
        field1 = Field.objects.create(label='f1', field_type='T', show_label=True, display=True, sort_order=1)
        field2 = Field.objects.create(label='f2', field_type='I', show_label=True, display=True, sort_order=2)
        for f in [field1, field2]:
            CardTemplates_Fields.objects.create(card_template=card_template, field=f)

        field_list = queries.getFieldList(collection.id)
        self.assertEqual(2, len(field_list))
        for idx, f in enumerate([field1, field2]):
            self.assertEqual(f.label, field_list[idx]['label'])
            self.assertEqual(f.field_type, field_list[idx]['field_type'])
            self.assertEqual(f.show_label, field_list[idx]['show_label'])
            self.assertEqual(f.display, field_list[idx]['display'])
            self.assertEqual(f.sort_order, field_list[idx]['sort_order'])

    def test_getDeckCardsList(self):
        card_template = CardTemplate.objects.create(title='b', description='bbb')
        collection = Collection.objects.create(title='a', description='aaa', card_template=card_template)
        field1 = Field.objects.create(label='f1', field_type='T', show_label=True, display=True, sort_order=1)
        field2 = Field.objects.create(label='f2', field_type='I', show_label=True, display=True, sort_order=2)
        for f in [field1, field2]:
            CardTemplates_Fields.objects.create(card_template=card_template, field=f)

        card_list = [
            [{"field_id":field1.id,"value":"a"},{"field_id":field2.id,"value":"http://www.columbia.edu/cu/arthistory/images/slideshow/Amiens.jpg"}],
            [{"field_id":field1.id,"value":"bb"},{"field_id":field2.id,"value":"http://www.columbia.edu/cu/arthistory/images/slideshow/10310749545.jpg"}],
            [{"field_id":field1.id,"value":"ccc"},{"field_id":field2.id,"value":"http://art.uga.edu/images/cache/ce_image/local/images/uploads/areas-of-study/overview/mfa_arthistory_overview_620_300auto_c1.jpg"}],
        ]
        deck_title = "my_deck_title"
        deck = services.create_deck_with_cards(collection.id, deck_title, card_list)

        self.assertEqual(deck_title, deck.title)
        self.assertEqual(len(card_list), deck.cards.count())

    def test_getDeckCollectionId(self):
        card_template = CardTemplate.objects.create(title='b', description='bbb')
        collection = Collection.objects.create(title='a', description='aaa', card_template=card_template)
        deck = Deck.objects.create(title='a', collection=collection)
        collection_id = queries.getDeckCollectionId(deck.id)

        self.assertEqual(collection.id, collection_id)
