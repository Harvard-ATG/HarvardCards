from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import services, queries, utils

def index(request, deck_id=None):
    """Displays the deck of cards for review/quiz."""
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

def delete(request, deck_id=None):
    """Deletes a deck."""
    collection_id = queries.getDeckCollectionId(deck_id)
    services.delete_deck(deck_id)
    return redirect('collection_id', collection_id)

def edit(request, deck_id=None):
    """Edits a deck."""
    deck = Deck.objects.get(id=deck_id)
    collections = Collection.objects.all()
    collection = Collection.objects.get(id=deck.collection.id)

    if request.method == 'POST':
        deck_form = DeckForm(request.POST, instance=deck)
        if deck_form.is_valid():
            deck = deck_form.save()
            return redirect(deck)
    else:
        deck_form = DeckForm(instance=deck)
        
    context = {
        "deck": deck,
        "deck_form": deck_form, 
        "collections": collections,
        "collection": collection
    }

    return render(request, 'decks/edit.html', context)
    
  
def download_deck(request, deck_id=None):
    '''
    Downloads an excel spreadsheet of a deck of cards.
    '''

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=flashcards.xls'

    file_output = utils.create_deck_file(deck_id) 
    response.write(file_output)

    return response
