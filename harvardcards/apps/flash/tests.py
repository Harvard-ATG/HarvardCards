from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.test.client import RequestFactory, Client
from django.contrib.auth.models import User
from django.http.request import HttpRequest

from django_auth_lti import const

from harvardcards.apps.flash.models import Collection, Deck, Field, CardTemplate, CardTemplates_Fields, Card, Canvas_Course_Map
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash.views.collection import *
from harvardcards.apps.flash import services, queries
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.settings.common import MEDIA_ROOT

import os
import unittest
import mock
import json

class CollectionTest(TestCase):
    admin_user = None
    admin_username = 'admintest'
    admin_password = 'password'
    admin_email = 'admintest@foo.us'

    def setUp(self):
        super(CollectionTest, self).setUp()
        self.factory = RequestFactory()
        self.client = Client()
        self._setupSuperUser()

    def tearDown(self):
        super(CollectionTest, self).tearDown()
        self.admin_user.delete()

    def _setupSuperUser(self):
        self.admin_user = User.objects.create_superuser(
                self.admin_username, 
                self.admin_email, 
                self.admin_password)

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
        logged_in = self.client.login(username=self.admin_user.username, password=self.admin_password)
        self.assertTrue(logged_in, 'super user logged in')

        card_template = CardTemplate(title="foobar_template")
        card_template.save()

        url = reverse('collectionCreate')
        post_data = {'title':'foobar', 'card_template':card_template.id}

        len_collections_before = len(Collection.objects.filter(title__exact=post_data['title']))
        response = self.client.post(url, post_data)
        len_collections_after = len(Collection.objects.filter(title__exact=post_data['title']))

        self.assertEqual(len_collections_before + 1, len_collections_after)

    def test_collection_form(self):
        card_template = CardTemplate(title="foobar_template")
        card_template.save()
        post_data = {'title':'foobar', 'card_template':card_template.id}
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
            [{"field_id":field1.id,"value":"a"},{"field_id":field2.id,"value":os.path.join(MEDIA_ROOT, 'tests', 'a.jpg')}],
            [{"field_id":field1.id,"value":"bb"},{"field_id":field2.id,"value":os.path.join(MEDIA_ROOT, 'tests', 'bb.jpg')}],
            [{"field_id":field1.id,"value":"ccc"},{"field_id":field2.id,"value":os.path.join(MEDIA_ROOT, 'tests', 'ccc.png')}],
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


class LTIServiceTest(TestCase):
    def setUp(self):
        """ Every test needs access to the request factory. """
        self.request = mock.Mock(spec=HttpRequest)
        self.request.session = {"LTI_LAUNCH":{}}
        pass

    def createMockRequest(self, canvas_course_id, roles):
        """ Creates a mock LTI launch request with the given canvas course ID and roles. """
        request = mock.Mock(spec=HttpRequest)
        request.session = {"LTI_LAUNCH":{
            "custom_canvas_course_id": canvas_course_id,
            "roles": roles 
        }}
        return request

    def test_isLTILaunch(self):
        request = mock.Mock(spec=HttpRequest)
        request.session = {"LTI_LAUNCH":{}}
        self.assertTrue(LTIService(request).isLTILaunch())

    def test_isNotLTILaunch(self):
        request = mock.Mock(spec=HttpRequest)
        request.session = {}
        self.assertFalse(LTIService(request).isLTILaunch())

    def test_associateCanvasCourse(self):
        card_template = CardTemplate.objects.create(title='Test', description='Test')
        collection = Collection.objects.create(title='Test', description='Test', card_template=card_template)

        canvas_course_id = 123
        request = self.createMockRequest(canvas_course_id, [const.INSTRUCTOR]) 
        lti_service = LTIService(request)

        self.assertFalse(lti_service.isCanvasCourseAssociated(canvas_course_id, collection.id), "Canvas course NOT associated with collection")
        result = lti_service.associateCanvasCourse(collection.id)
        self.assertTrue(result, msg="Canvas course associated successfully")
        self.assertTrue(lti_service.isCanvasCourseAssociated(canvas_course_id, collection.id), "Canvas course IS associated with collection")

    def test_subscribeToCourseCollections(self):
        card_template = CardTemplate.objects.create(title='Test', description='Test')
        a_collection = Collection.objects.create(title='Test', description='Test', card_template=card_template)
        b_collection = Collection.objects.create(title='Test2', description='Test2', card_template=card_template)
        c_collection = Collection.objects.create(title='Test3', description='Test3', card_template=card_template)
        d_collection = Collection.objects.create(title='Test4', description='Test4', card_template=card_template)

        canvas_course_id = 123
        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        request = self.createMockRequest(canvas_course_id, [const.LEARNER]) 
        request.user = user

        Canvas_Course_Map.objects.create(canvas_course_id=canvas_course_id, collection=a_collection, subscribe=True)
        Canvas_Course_Map.objects.create(canvas_course_id=canvas_course_id, collection=b_collection, subscribe=True)
        Canvas_Course_Map.objects.create(canvas_course_id=canvas_course_id, collection=c_collection, subscribe=False)
        Canvas_Course_Map.objects.create(canvas_course_id=canvas_course_id + 1, collection=d_collection, subscribe=True)

        self.assertTrue(LTIService(request).subscribeToCourseCollections())
        subscribed = Users_Collections.objects.filter(user=user)
        self.assertEqual(len(subscribed), 2)
        self.assertFalse(Users_Collections.objects.filter(user=user,collection=c_collection))

    def test_getCourseCollections(self):
        card_template = CardTemplate.objects.create(title='Test', description='Test')
        collection = Collection.objects.create(title='Test', description='Test', card_template=card_template)
        collection2 = Collection.objects.create(title='Test2', description='Test2', card_template=card_template)
        collection3 = Collection.objects.create(title='Test3', description='Test3', card_template=card_template)

        canvas_course_id = 123
        request = self.createMockRequest(canvas_course_id, [const.INSTRUCTOR]) 
        lti_service = LTIService(request)

        self.assertTrue(lti_service.associateCanvasCourse(collection.id))
        self.assertTrue(lti_service.associateCanvasCourse(collection3.id))

        self.assertTrue(lti_service.isCanvasCourseAssociated(canvas_course_id, collection.id))
        self.assertFalse(lti_service.isCanvasCourseAssociated(canvas_course_id, collection2.id))
        self.assertTrue(lti_service.isCanvasCourseAssociated(canvas_course_id, collection3.id))

        canvas_collections = lti_service.getCourseCollections()
        expected_collections = [c.id for c in (collection, collection3)]
        self.assertEqual(len(canvas_collections), len(expected_collections))
        self.assertEqual(canvas_collections, expected_collections)
