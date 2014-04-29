from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm, DeckImportForm
from harvardcards.apps.flash import services, queries, utils

import urllib

def index(request, deck_id=None):
    """Displays the deck of cards for review/quiz."""
    collections = Collection.objects.all().prefetch_related('deck_set')
    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')
    current_collection = Collection.objects.get(id=deck.collection.id)
    user_collection_role = Users_Collections.get_role_buckets(request.user, collections)
    is_quiz_mode = request.GET.get('mode') == 'quiz'
    is_deck_admin = next((True for cid in user_collection_role['ADMIN'] if cid == current_collection.id), False)
    card_id = request.GET.get('card_id', '')

    cards = []
    for dcard in deck_cards:
        card_fields = {'show':[],'reveal':[]}
        for cfield in dcard.card.cards_fields_set.all():
            if cfield.field.display:
                bucket = 'show'
            else:
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
        "collection": current_collection,
        "collections": collections,
        "deck": deck,
        "cards": cards,
        "is_quiz_mode": is_quiz_mode,
        "is_deck_admin": is_deck_admin,
        "card_id": card_id
    }

    return render(request, "deck_view.html", context)

def delete(request, deck_id=None):
    """Deletes a deck."""
    collection_id = queries.getDeckCollectionId(deck_id)
    services.delete_deck(deck_id)
    return redirect('collectionIndex', collection_id)

def upload_deck(request, deck_id=None):
    '''
    Imports a deck of cards from an excel spreadsheet.
    '''
    deck = Deck.objects.get(id=deck_id)
    collections = Collection.objects.all()
    collection = Collection.objects.get(id=deck.collection.id)

    if request.method == 'POST':
        deck_form = DeckImportForm(request.POST, request.FILES)
        if deck_form.is_valid():
            if 'file' in request.FILES:
                services.handle_uploaded_deck_file(deck, request.FILES['file'])
            return redirect(deck)
    else:
        deck_form = DeckImportForm()

    context = {
        "deck": deck,
        "deck_form": deck_form, 
        "collections": collections,
        "collection": collection
    }

    return render(request, 'decks/upload.html', context)

def download_deck(request, deck_id=None):
    '''
    Downloads an excel spreadsheet of a deck of cards.
    '''

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=flashcards.xls'

    file_output = utils.create_deck_file(deck_id) 
    response.write(file_output)

    return response

def edit_card(request, deck_id=None):
    """Add a new card to the deck."""
    deck = Deck.objects.get(id=deck_id)
    current_collection = Collection.objects.get(id=deck.collection.id)
    collections = Collection.objects.all().prefetch_related('deck_set')

    if request.method == 'POST':
        errorMsg = ''
        field_prefix = 'field_'
        fields = []
        for field_name, field_value in request.FILES.items():
            if field_name.startswith(field_prefix):
                field_id = field_name.replace(field_prefix, '')
                if field_id.isdigit():
                    if request.FILES[field_name].size > 0:
                        path = services.handle_uploaded_img_file(request.FILES[field_name], deck.id, deck.collection.id)
                        fields.append({"field_id": int(field_id), "value": path})

        for field_name, field_value in request.POST.items():
            if field_name.startswith(field_prefix):
                field_id = field_name.replace(field_prefix, '')
                if field_id.isdigit():
                    fields.append({"field_id": int(field_id), "value": field_value})

        if request.POST.get('card_id', '') == '':
            card = services.add_card_to_deck(deck, fields)
        else:
            card = Card.objects.get(id=request.POST.get('card_id'))
            services.update_card_fields(card, fields)

        params = {"card_id":card.id}
        return redirect(deck.get_absolute_url() + '?' + urllib.urlencode(params))

    card_fields = {'show':[],'reveal':[]}
    if request.GET.get('card_id', '') == '':
        for field in current_collection.card_template.fields.all():
            if field.display:
                bucket = 'show'
            else:
                bucket = 'reveal'
            card_fields[bucket].append({
                'id': field.id,
                'type': field.field_type,
                'label': field.label,
                'show_label': field.show_label,
                'value': ''
            })
    else:
        card = Card.objects.get(id=request.GET.get('card_id'))
        for cfield in card.cards_fields_set.all():
            if cfield.field.display:
                bucket = 'show'
            else:
                bucket = 'reveal'
            card_fields[bucket].append({
                'id': cfield.field.id,
                'type': cfield.field.field_type,
                'label': cfield.field.label,
                'show_label': cfield.field.show_label,
                'value': cfield.value,
            })

    context = {
        "deck": deck,
        "card_id": request.GET.get('card_id', ''),
        "collection": current_collection,
        "collections": collections,
        "card_fields": card_fields,
    }

    return render(request, 'decks/edit_card.html', context)

@require_http_methods(["POST"])
def delete_card(request, deck_id=None):
    """Deletes a card."""
    deck = Deck.objects.get(id=deck_id)
    card_id = request.POST.get('card_id', None)
    success = services.delete_card(card_id)
    return redirect(deck)
