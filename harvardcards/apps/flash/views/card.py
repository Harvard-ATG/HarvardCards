from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Card, Field, Decks_Cards, Cards_Fields
from harvardcards.apps.flash.forms import FieldForm

def create(request):
    errorMsg = ''
    if 'collection_id' in request.POST:
        collection_id = request.POST['collection_id']
        
        if 'deck_id' in request.POST:
            deck_id = request.POST['deck_id']
        
            if 'card_id' in request.POST:

            
                if 'fields' in request.POST:

                    if request.POST['card_id'] != '':
                        card = Card.objects.get(id=request.POST['card_id'])
                    else: 
                        collection = Collection.objects.get(id=collection_id)
                        # TODO: sort_order
                        card = Card(collection=collection, sort_order=0)
                        card.save()



                    data = json.loads(request.POST['fields'])
                    # run through the field data to create/edit new Cards_Fields
                    fc_sort_order = 0
                    for d in data:
                        field = Field.objects.get(id=d['field_id'])
                        fc = Cards_Fields(value=d['value'], field=field, card=card, sort_order=fc_sort_order)
                        fc.save();
                        fc_sort_order += 1
                    
                    # create decks_cards connection
                    # TODO: sort_order
                    deck = Deck.objects.get(id=deck_id)
                    dc = Decks_Cards(deck=deck, card=card, sort_order=0)
                    dc.save()
                    
            
                else:
                    errorMsg = "Field data not provided."
                    for key in request.POST:
                        value = request.POST[key]
                        errorMsg += "\n{0} => {1}".format(key, value)
                    
            else:
                errorMsg = "card_id not provided"
        else:
            errorMsg = "deck_id not provided"
        
        
    else:
        errorMsg = "collection_id not provided."
    
        
    
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
    