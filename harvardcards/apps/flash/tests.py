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
from django.core.files.uploadedfile import SimpleUploadedFile

from django_auth_lti import const

from harvardcards.apps.flash.models import Collection, Deck, Field, CardTemplate, CardTemplates_Fields, Card, Canvas_Course_Map, Users_Collections
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash.views.collection import *
from harvardcards.apps.flash import services, queries
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.settings.common import MEDIA_ROOT

import os
import unittest
import mock
import json
import zipfile

TESTFIXTURES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests', 'testfixtures')

class CollectionTest(TestCase):
    admin_user = None
    admin_username = 'admintest'
    admin_password = 'password'
    admin_email = 'admintest@foo.us'

    def setUp(self):
        super(CollectionTest, self).setUp()
        self.factory = RequestFactory()
        self.client = Client()
        self.card_template = CardTemplate.objects.create(title='b', description='bbb')
        self._setupSuperUser()

    def tearDown(self):
        super(CollectionTest, self).tearDown()
        if self.admin_user:
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

    def test_collection_get(self):
        url = reverse('collectionIndex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_collection_create(self):
        logged_in = self.client.login(username=self.admin_user.username, password=self.admin_password)
        self.assertTrue(logged_in, 'super user logged in')

        url = reverse('collectionCreate')
        post_data = {'title':'foobar', 'card_template':self.card_template.id}

        self.assertFalse(Collection.objects.filter(title__exact=post_data['title']))
        response = self.client.post(url, post_data)
        self.assertTrue(Collection.objects.filter(title__exact=post_data['title']))

    def test_collection_form(self):
        form = CollectionForm({"title":"foo","card_template":self.card_template.id})
        self.assertTrue(form.is_valid())

        form1 = CollectionForm({})
        self.assertFalse(form1.is_valid())

class ServicesTest(TestCase):
    def setUp(self):
        """ Every test needs access to the request factory. """
        self.factory = RequestFactory()
        self.client = Client()
        self.card_template = CardTemplate.objects.create(title='b', description='bbb')
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

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

    def test_addUserToCollection(self):
        collection = self.makeCollection()
        user = self.user
        role = Users_Collections.LEARNER

        success = services.add_user_to_collection(user=user, collection=collection, role=role)
        self.assertTrue(success)
        self.assertTrue(Users_Collections.objects.filter(user=user, collection=collection, role=role))

    def make_uploaded_zip_file(self, filename):
        path = os.path.join(TESTFIXTURES_DIR, filename)
        content_type = 'application/zip'
        content = ''
        with open(path) as f:
            content = f.read()

        return SimpleUploadedFile.from_dict({
            'filename': filename,
            'content': content,
            'content-type': content_type,
        })

    def test_extract_zip_xls_and_images(self):
        filename = 'xls_and_images.zip'
        uploaded_file = self.make_uploaded_zip_file(filename)
        self.assertTrue(uploaded_file)
        self.assertEqual(uploaded_file.name, filename)
        self.assertEqual(uploaded_file.content_type, 'application/zip')

        # expect all files to be compressed directly (i.e. no containing folder)
        expected_path_to_excel = '' 

        # expect these files to be extracted from zip file
        expected_file_names = [
            'BartSimpson4.gif',
            'MaggieSimpson1.gif',
            'flashcards_template.xls'
        ]

        result = services.extract_from_zip(uploaded_file)
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(isinstance(result[1], zipfile.ZipFile))
        self.assertEqual(result[2], expected_file_names)
        self.assertEqual(result[3], expected_path_to_excel)

    def test_extract_zip_folder_with_xls_and_images(self):
        filename = 'folder_with_xls_and_images.zip'
        uploaded_file = self.make_uploaded_zip_file(filename)
        self.assertTrue(uploaded_file)
        self.assertEqual(uploaded_file.name, filename)
        self.assertEqual(uploaded_file.content_type, 'application/zip')

        # expect all files to be compressed directly (i.e. no containing folder)
        expected_path_to_excel = 'folder_with_xls_and_images' 

        # expect these files to be extracted from zip file
        expected_file_names = [
            'folder_with_xls_and_images/',
            'folder_with_xls_and_images/.DS_Store',
            'folder_with_xls_and_images/BartSimpson4.gif',
            'folder_with_xls_and_images/MaggieSimpson1.gif',
            'folder_with_xls_and_images/flashcards_template.xls'
        ]

        result = services.extract_from_zip(uploaded_file)
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(isinstance(result[1], zipfile.ZipFile))
        self.assertEqual(result[2], expected_file_names)
        self.assertEqual(result[3], expected_path_to_excel)

    def test_extract_zip_folder_with_xls_and_audio(self):
        filename = 'folder_with_xls_and_audio_folder.zip'
        uploaded_file = self.make_uploaded_zip_file(filename)
        self.assertTrue(uploaded_file)
        self.assertEqual(uploaded_file.name, filename)
        self.assertEqual(uploaded_file.content_type, 'application/zip')

        # expect all files to be compressed directly (i.e. no containing folder)
        expected_path_to_excel = 'folder_with_xls_and_audio_folder' 

        # expect these files to be extracted from zip file
        expected_file_names = [
            'folder_with_xls_and_audio_folder/',
            'folder_with_xls_and_audio_folder/.DS_Store',
            'folder_with_xls_and_audio_folder/audio/',
            'folder_with_xls_and_audio_folder/audio/aurevoir.mp3',
            'folder_with_xls_and_audio_folder/audio/bonappetit.mp3',
            'folder_with_xls_and_audio_folder/audio/bonjour.mp3',
            'folder_with_xls_and_audio_folder/audio/double.mp3',
            'folder_with_xls_and_audio_folder/audio/horsdoeuvre.mp3',
            'folder_with_xls_and_audio_folder/audio/jenecomprendspas.mp3',
            'folder_with_xls_and_audio_folder/deck.xls'
        ]

        result = services.extract_from_zip(uploaded_file)
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(isinstance(result[1], zipfile.ZipFile))
        self.assertEqual(result[2], expected_file_names)
        self.assertEqual(result[3], expected_path_to_excel)

class QueriesTest(TestCase):
    def setUp(self):
        """ Every test needs access to the request factory. """
        self.factory = RequestFactory()
        self.client = Client()
        self.card_template = CardTemplate.objects.create(title='b', description='bbb')

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
