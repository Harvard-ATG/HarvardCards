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
    print request.POST
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
                    card_data = {}
                    card_data['card_id'] = card.id
                    #card_data['first_label'] = data[0].label
                    card_data['first_value'] = data[0]['value']
                    
                    return HttpResponse('{"success": true, "card_data": %s}' % json.dumps(card_data), mimetype="application/json")
                    
                else:
                    errorMsg = "Field data not provided."
            else:
                errorMsg = "card_id not provided"
        else:
            errorMsg = "deck_id not provided"
        
        
    else:
        errorMsg = "collection_id not provided."
    
        
    
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
    

def fields(request):
    errorMsg = ''
    # get the card id
    if 'card_id' in request.POST:
        card_id = request.POST['card_id']
        card = Card.objects.get(id=card_id)
        cfs = Cards_Fields.objects.filter(card=card).order_by('sort_order')
        fields = []
        for cf in cfs:
            field = {}
            field['value'] = cf.value
            field['label'] = cf.field.label
            field['display'] = cf.field.display
            field['field_type'] = cf.field.field_type
            field['field_id'] = cf.field.id
            field['cards_fields_id'] = cf.id
            fields.append(field)
        fields_json = json.dumps(fields)
        return HttpResponse('{"success": true, "fields": %s}' % fields_json, mimetype="application/json")
    else:
        errorMsg = "card_id not provided."
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
    
def delete(request):
    errorMsg = ''
    if 'card_id' in request.POST:
        card_id = request.POST['card_id']
        card = Card.objects.get(id=card_id)
        card.delete()
        return HttpResponse('{"success": true}', mimetype="application/json")
    else:
        errorMsg = "card_id not provided."
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")

def fieldEdit(request):
    errorMsg = ''
    if 'cards_fields_id' in request.POST:
        if 'value' in request.POST:
            cf_id = request.POST['cards_fields_id']
            value = request.POST['value']
            cf = Cards_Fields.objects.get(id=cf_id)
            cf.value = value
            cf.save()
            return HttpResponse('{"success": true}', mimetype="application/json")
        else:
            errorMsg = "value not provided."
    else:
        errorMsg = "cards_fields_id not provided."
        
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
    
    