from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm

def index(request, deck_id=None):
    collections = Collection.objects.all()    
    if not deck_id:
        # then it's a create
        # and if it's a create, the request should be a post with the collection_id in it
        if 'collection_id' in request.POST:
            collection_id = request.POST['collection_id']
        return render(request, "decks/index.html", {"collection_id": collection_id, "collections": collections, "deck": {"id": "true", "title": "spamatam"}})
    
    deck = Deck.objects.get(id=deck_id)
    
    return render(request, "decks/index.html", {"collections": collections, "deck": deck, "collection_id": deck.collection.id})

# 
def create(request, deck_id=None):
    if request.method == 'POST':
        if 'deck_id' in request.POST:
            # then it's an edit
            deck = Deck.objects.get(id=request.POST['deck_id'])
            deck_id = request.POST['deck_id']
            deckForm = DeckForm(request.POST, instance=deck)
            collection_id = deck.collection.id
        else:
            # then it's a new one
            deckForm = DeckForm(request.POST)
            collection_id = request.POST['collection_id']
            
        deckForm = DeckForm(request.POST)
        if deckForm.is_valid():
            deck = deckForm.save(commit=False)
            deck.collection = Collection.objects.get(id=collection_id)
            if deck_id:
                deck.id = deck_id
            deck.save()
            if deck:
                return HttpResponse('{"success": true}', mimetype="application/json")
            else:
                errorMsg = 'Failure to save.'
        else:
            errorMsg = 'Validation Error.'
    else:
        errorMsg = 'Invalid Request.'
    return HttpResponse('{"success": false, "message": {0}}'.format(errorMsg))

def delete(request):
    returnValue = "false"
    if request.POST['deck_id']:
        deck_id = request.POST['deck_id']
        Deck.objects.filter(id=deck_id).delete()
        if not Deck.objects.filter(id=deck_id):
            returnValue = "true"
    
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
  
