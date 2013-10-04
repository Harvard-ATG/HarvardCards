from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json
from django.test import TestCase

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from django.test.client import RequestFactory
from harvardcards.apps.flash.views.collection import *

class CollectionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
    def test_collection(self):
        title = "title of card"
        des = "nothing in description"
        collection = create({"title": title, "description": des}, collection_id=1)
        delt = delete({"id":1})
        TestCase.assertEqual(HTTPResponse('{"success": "true"}', mimetype="application/json"), delt)