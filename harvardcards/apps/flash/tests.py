from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.test.client import RequestFactory, Client

from harvardcards.apps.flash.models import Collection, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash.views.collection import *

class CollectionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_collection_get(self):
        url = reverse('create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/create.html')

    def test_collection_post(self):
        # there should be no collections at the start
        len_collection1 = len(Collection.objects.all())
        self.assertEqual(len_collection1, 0)

        # url for create collection
        url = reverse('create')

        # sample post data
        post_data = {'field_data': '[{"field_type":"T","label":"","sort_order":0,"display":true},{"field_type":"I","label":"","sort_order":1,"display":true},{"field_type":"T","label":"","sort_order":2,"display":false}]', 'csrfmiddlewaretoken': '38vLxTwts8C4pUcFqoOgQAq3eXgAdpro', 'field_type1': 'text', 'description': 'lots of math', 'title': 'math 454'}

        # response of posting the data at url
        response = self.client.post(url, post_data)
        # should redirect to index
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response,'index.html')

        # number of collections should be 1 now
        len_collection2 = len(Collection.objects.all())
        self.assertEqual(len_collection2, 1)
        self.assertEqual(len_collection2-len_collection1, 1)

    def test_collection_form(self):
        post_data = {'field_data': '[{"field_type":"T","label":"","sort_order":0,"display":true},{"field_type":"I","label":"","sort_order":1,"display":true},{"field_type":"T","label":"","sort_order":2,"display":false}]', 'csrfmiddlewaretoken': '38vLxTwts8C4pUcFqoOgQAq3eXgAdpro', 'field_type1': 'text', 'description': 'lots of math', 'title': 'math 454'}
        # testing the form
        form = CollectionForm(post_data)
        self.assertEqual(form.is_valid(), True)
        form1 = CollectionForm({})
        self.assertEqual(form1.is_valid(), False)


