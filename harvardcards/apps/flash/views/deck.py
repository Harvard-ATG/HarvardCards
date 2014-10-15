from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.forms.formsets import formset_factory
from django.forms import widgets
from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm, DeckImportForm
from harvardcards.apps.flash import services, queries, utils
from harvardcards.apps.flash.services import check_role

from PIL import Image
import urllib
import json

def index(request, deck_id=None):
    """Displays the deck of cards for review/quiz."""

    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')
    current_collection = deck.collection 

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

    is_quiz_mode = request.GET.get('mode') == 'quiz'
    is_deck_admin = current_collection.id in role_bucket['ADMINISTRATOR']
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
            'color': dcard.card.color,
            'fields': card_fields
            })

    context = {  
        "collection": current_collection,
        "nav_collections": collection_list,
        "deck": deck,
        "cards": cards,
        "is_quiz_mode": is_quiz_mode,
        "is_deck_admin": is_deck_admin,
        "card_id": card_id,
    }

    return render(request, "deck_view.html", context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def delete(request, deck_id=None):
    """Deletes a deck."""

    collection_id = queries.getDeckCollectionId(deck_id)
    services.delete_deck(deck_id)
    response =  redirect('collectionIndex', collection_id)
    response['Location'] += '?instructor=edit'
    return response

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def upload_deck(request, deck_id=None):
    '''
    Imports a deck of cards from an excel spreadsheet.
    '''
    
    deck = Deck.objects.get(id=deck_id)
    current_collection = deck.collection

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

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
            "nav_collections": collection_list,
            "collection": current_collection
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

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def create_edit_card(request, deck_id=None):
    """Create a new card or edit an existing one from the collection card template."""

    IMAGE_UPLOAD_TYPE = (('F', 'File'),('U', 'URL'))

    deck = Deck.objects.get(id=deck_id)
    current_collection = deck.collection
    card_color_select = widgets.Select(attrs=None, choices=Card.COLOR_CHOICES)
    image_upload_select = widgets.Select(attrs= {'onchange' :'switch_upload_image_type(this)'}, choices=IMAGE_UPLOAD_TYPE)

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

    # Only has card_id if we are editing a card
    card_id = request.GET.get('card_id', '')
    if card_id:
        card = Card.objects.get(id=card_id)
        card_color = card.color
    else:
        card_color = Card.DEFAULT_COLOR

    if card_id:
        field_list = [{
            "id":cfield.field.id, 
            "type": cfield.field.field_type,
            "label": cfield.field.label,
            "bucket": "show" if cfield.field.display else "reveal",
            "show_label": cfield.field.show_label,
            "value": cfield.value
        } for cfield in card.cards_fields_set.all()]
    else:
        field_list = [{
            "id": field.id, 
            "type": field.field_type,
            "bucket": "show" if field.display else "reveal",
            "label": field.label,
            "show_label": field.show_label,
            "value": ""
        } for field in current_collection.card_template.fields.all()]

    card_fields = {'show':[], 'reveal':[]}
    for field in field_list:
        card_fields[field['bucket']].append(field)

    context = {
        "deck": deck,
        "card_id": card_id if card_id else '',
        "collection": current_collection,
        "nav_collections": collection_list,
        "card_fields": card_fields,
        "card_color_select":  card_color_select.render("card_color", card_color),
        "upload_type_select": image_upload_select.render("image_upload", 'F')
    }
    
    return render(request, 'decks/edit_card.html', context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def delete_card(request, deck_id=None):
    """Deletes a card."""

    deck = Deck.objects.get(id=deck_id)
    card_id = request.GET.get('card_id', None)
    if queries.isCardInDeck(card_id, deck_id):
        success = services.delete_card(card_id)
    return redirect(deck)
