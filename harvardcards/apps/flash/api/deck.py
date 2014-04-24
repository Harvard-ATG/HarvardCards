from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import redirect

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash import forms, services, queries, utils
from django.db import models

@require_http_methods(["POST"])
def delete(request, deck_id=None):
    """Delete a deck"""
    result = {"success": False}
    if deck_id is not None:
        collection_id = queries.getDeckCollectionId(deck_id)
        result['success'] = services.delete_deck(deck_id)
        redirect_response = redirect('collectionIndex', collection_id)
        result['location'] = redirect_response['Location']
    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["POST"])
def rename(request, deck_id=None):
    """Rename a deck"""
    result = {"success": False}
    if deck_id is not None:
        deck = Deck.objects.get(id=deck_id)
        deck_form = forms.DeckForm(request.POST, instance=deck)
        result['success'] = deck_form.is_valid()
        if deck_form.is_valid():
            deck = deck_form.save()
        else:
            result['errors'] = {'title': deck_form['title'].errors}
    return HttpResponse(json.dumps(result), mimetype="application/json")