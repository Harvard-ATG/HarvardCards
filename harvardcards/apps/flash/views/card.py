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

            if 'max_card_id' in request.POST:

                card_id = int(request.POST['max_card_id']) + 1
                if 'num_fields' in request.POST:

                    # if request.POST['card_id'] != '':
                    #     card = Card.objects.get(id=request.POST['card_id'])
                    # else:
                    collection = Collection.objects.get(id=collection_id)
                    # TODO: sort_order
                    collection_sort_order =  len(Card.objects.filter(collection_id=collection_id)) + 1
                    card = Card(collection=collection, sort_order=collection_sort_order)
                    card.save()

                    for i in range(0, int(request.POST['num_fields'])):
                        numfield = str(i+1)
                        value = request.POST['Value'+numfield]
                        if request.POST.get('Label'+numfield, 0):
                            label = request.POST['Label'+numfield]
                        else:
                            label = ''

                        field_type = request.POST['Field Type'+numfield]
                        if request.POST.get('display'+numfield, 0):
                            display = True
                        else:
                            display = False
                        if request.POST.get('showLabel'+numfield, 0):
                            show_label = True
                        else:
                            show_label = False
                        fd = Field(field_type=field_type, show_label= show_label, collection= collection, label= label, sort_order= i+1, display=display)
                        fd.save()

                        cardfield = Cards_Fields(value=value, field = fd, card = card, sort_order = i+1)
                        cardfield.save()
                    # data = json.loads(request.POST['fields'])
                    # # run through the field data to create/edit new Cards_Fields
                    # fc_sort_order = 0
                    # for d in data:
                    #     field = Field.objects.get(id=d['field_id'])
                    #     fc = Cards_Fields(value=d['value'], field=field, card=card, sort_order=fc_sort_order)
                    #     fc.save();
                    #     fc_sort_order += 1
                    #
                    # # create decks_cards connection
                    # # TODO: sort_order
                    deck = Deck.objects.get(id=deck_id)
                    dc = Decks_Cards(deck=deck, card=card, sort_order=card_id)
                    dc.save()
                    # card_data = {}
                    # card_data['card_id'] = card.id
                    # #card_data['first_label'] = data[0].label
                    # card_data['first_value'] = data[0]['value']
                    if request.POST['quiz_mode']=='True':
                        path = '/deck/'+str(deck_id)+'?mode=quiz&cardLoc='+str(card_id)
                    else:
                        path = '/deck/'+str(deck_id)+'?cardLoc='+str(card_id)
                    return redirect(path)
                    
                else:
                    errorMsg = "num_fields not provided."
            else:
                errorMsg = "max_card_id not provided"
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
    
    