from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import queries, utils

def test1(request):
    return render(request, "decks/test1.html")

def test2(request):
    return render(request, "decks/test2.html")

def index(request, deck_id=None):
    collections = Collection.objects.all().prefetch_related('deck_set')
    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')
    current_collection = Collection.objects.get(id=deck.collection.id)
    user_collection_role = Users_Collections.get_role_buckets(request.user, collections)
    is_quiz_mode = request.GET.get('mode') == 'quiz'

    cards = []
    for dcard in deck_cards:
        card_fields = {'show':[],'reveal':[]}
        for cfield in dcard.card.cards_fields_set.all():
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
        "user_collection_role": user_collection_role,
        "collections": collections,
        "deck": deck,
        "cards": cards,
        "collection": current_collection,
        "is_quiz_mode": is_quiz_mode
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
                #return HttpResponse('{"success": true, "id": %s}' % deck.id, mimetype="application/json")
                object = Deck.objects.get(id = deck.id)
                return redirect(object)
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
  
def download_deck(request, deck_id=None):
    '''
    Downloads an excel spreadsheet of a deck of cards.
    '''

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=flashcards.xls'

    file_output = utils.create_deck_file(deck_id) 
    response.write(file_output)

    return response
