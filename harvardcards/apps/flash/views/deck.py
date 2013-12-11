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
    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card')

    cards = []
    for dcard in deck_cards:
        card_fields = {'show':[],'reveal':[]}
        for cfield in dcard.card.cards_fields_set.all().order_by('sort_order'):
            bucket = 'show'
            if cfield.field.display:
                bucket = 'reveal'
            card_fields[bucket].append({
                'type': cfield.field.field_type,
                'label': cfield.field.label,
                'show_label': cfield.field.show_label,
                'value': cfield.value,
            })
        cards.append({
            'card_id': dcard.card.id,
            'fields': card_fields
        })

    context = {
        "collections": collections,
        "deck": deck,
        "cards": cards
    }

    return render(request, "deck_view.html", context)

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
  
