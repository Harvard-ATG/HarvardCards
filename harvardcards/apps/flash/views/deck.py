from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm

def test1(request):
    return render(request, "decks/test1.html")

def test2(request):
    return render(request, "decks/test2.html")

def index(request, deck_id=None):
    collections = Collection.objects.all()  
    if not deck_id:
        # then it's a create
        # and if it's a create, the request should be a post with the collection_id in it
        if 'collection_id' in request.POST:
            collection_id = request.POST['collection_id']
            current_collection = Collection.objects.get(id=collection_id)
        else:
            raise ViewDoesNotExist
        deck = None
        cards = None
    else:
        deck = Deck.objects.get(id=deck_id)
        current_collection = Collection.objects.get(id=deck.collection.id)
        #deck_cards = Deck.objects.card_set.all()
        #decks_cards = Deck.objects.filter(deck=deck)
        deck_cards = Decks_Cards.objects.filter(deck=deck)
        cards = []
        for dc in deck_cards:
            card_dict = {}
            card_dict['card_id'] = dc.card.id
            cf = dc.card.cards_fields_set.all()[0]
            card_dict['first_label'] = cf.field.label
            card_dict['first_value'] = cf.value
            cards.append(card_dict)
        
        #Decks_Cards.objects.filter(deck=deck).card.all()
    return render(request, "decks/index.html", 
        {"collections": collections, "deck": deck, "cards": cards, 
        "collection_id": current_collection.id, "collection": current_collection})

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
                return HttpResponse('{"success": true, "id": %s}' % deck.id, mimetype="application/json")
            else:
                errorMsg = 'Failure to save.'
        else:
            errorMsg = 'Validation Error.'
    else:
        errorMsg = 'Invalid Request.'
    return HttpResponse('{"success": false, "message": {0}}'.format(errorMsg), mimetype="application/json")

def delete(request):
    returnValue = "false"
    if request.POST['deck_id']:
        deck_id = request.POST['deck_id']
        Deck.objects.filter(id=deck_id).delete()
        if not Deck.objects.filter(id=deck_id):
            returnValue = "true"
    
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
  
