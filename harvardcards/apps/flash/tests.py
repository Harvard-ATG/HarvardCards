from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from django.test.client import RequestFactory, Client
from harvardcards.apps.flash.views.collection import *

class CollectionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        collections = Collection.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_collection(self):
        title = "title of card"
        des = "nothing in description"

        TestCase.assertEqual()