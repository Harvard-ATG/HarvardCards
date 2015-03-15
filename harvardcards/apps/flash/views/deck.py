from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.forms import widgets

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Users_Collections
from harvardcards.apps.flash.forms import DeckImportForm
from harvardcards.apps.flash.decorators import check_role
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.apps.flash import services, queries, analytics

import logging
log = logging.getLogger(__name__)

def deck_view_helper(request, current_collection, deck_cards):

    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

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
    return [cards, collection_list, is_quiz_mode, is_deck_admin, card_id]


def index(request, deck_id=None):
    """Displays the deck of cards for review/quiz."""

    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')
    current_collection = deck.collection
    [cards, collection_list, is_quiz_mode, is_deck_admin, card_id] = deck_view_helper(request, current_collection, deck_cards)

    context = {  
        "collection": current_collection,
        "nav_collections": collection_list,
        "deck": deck,
        "cards": cards,
        "is_quiz_mode": is_quiz_mode,
        "is_deck_admin": is_deck_admin,
        "card_id": card_id,
    }

    analytics.track(
        actor=request.user,
        verb=analytics.VERBS.viewed,
        object=analytics.OBJECTS.deck,
        context={"deck_id": deck_id},
    )
    return render(request, "deck_view.html", context)

def all_cards(request, collection_id):
    collection_id = int(collection_id)
    decks = queries.getDecksByCollection(collection_ids = [collection_id])
    decks = decks[collection_id]
    current_collection = Collection.objects.get(id=collection_id)

    deck_cards = []
    for deck in decks:
        deck_cards += Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')
    [cards, collection_list, is_quiz_mode, is_deck_admin, card_id] = deck_view_helper(request, current_collection, deck_cards)
    context = {
        "collection": current_collection,
        "nav_collections": collection_list,
        "deck": {'id': -collection_id, 'title': 'All Cards'},
        "cards": cards,
        "is_quiz_mode": is_quiz_mode,
        "is_deck_admin": is_deck_admin,
        "card_id": card_id,
    }
    analytics.track(
        actor=request.user,
        verb=analytics.VERBS.viewed,
        object=analytics.OBJECTS.deck,
        context={"collection_id": collection_id, 'type': 'All Cards Deck'},
    )
    return render(request, "deck_view.html", context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def delete(request, deck_id=None):
    """Deletes a deck."""
    d = {'user': request.user}

    collection_id = queries.getDeckCollectionId(deck_id)
    success = services.delete_deck(deck_id)
    if success:
        log.info('Deck %(d)s deleted from collection %(c)s' %{'d':deck_id, 'c':collection_id}, extra=d)
    else:
        log.info('Deck %(d)s could not be deleted from collection %(c)s' %{'d':deck_id, 'c':collection_id}, extra=d)

    response =  redirect('collectionIndex', collection_id)
    response['Location'] += '?instructor=edit'

    analytics.track(
        actor=request.user,
        verb=analytics.VERBS.deleted,
        object=analytics.OBJECTS.deck,
        context={"deck_id": deck_id},
    )

    return response

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def upload_deck(request, deck_id=None):
    '''
    Imports a deck of cards from an excel spreadsheet.
    '''
    upload_error = ''
    deck = Deck.objects.get(id=deck_id)
    current_collection = deck.collection

    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

    if request.method == 'POST':
        d = {'user': request.user}
        log.info('The user is uploading a new deck.', extra=d)
        deck_form = DeckImportForm(request.POST, request.FILES)
        if deck_form.is_valid():
            if 'file' in request.FILES:
                try:
                    services.handle_uploaded_deck_file(deck, request.FILES['file'])
                    log.info('New deck successfully added to the collection %(c)s.' %{'c': str(deck.collection.id)}, extra=d)
                    analytics.track(
                        actor=request.user,
                        verb=analytics.VERBS.uploaded,
                        object=analytics.OBJECTS.deck,
                        context={"deck_id": deck_id},
                    )
                    return redirect(deck)
                except Exception, e:
                    upload_error = str(e)
                    msg = 'The following error occurred when the user tried uploading a deck: '
                    log.error(msg + upload_error, extra=d)
            else:
                log.info('No file selected.', extra=d)
        else:
            log.error('Deck Form is not valid.', extra=d)

    else:
        deck_form = DeckImportForm()

    context = {
            "deck": deck,
            "deck_form": deck_form, 
            "nav_collections": collection_list,
            "collection": current_collection,
            "upload_error": upload_error
            }
    return render(request, 'decks/upload.html', context)

def download_deck(request, deck_id=None):
    '''
    Downloads a ZIP containing the excel spreadsheet of the deck of cards
    along with any associated media files like images or audio.
    '''

    deck =  Deck.objects.get(id=deck_id)
    zfile_output = services.create_zip_deck_file(deck)
    log.info('Deck %(d)s from the collection %(c)s downloaded by the user.'
            %{'d': str(deck.id), 'c': str(deck.collection.id)}, extra={'user': request.user})

    response = HttpResponse(zfile_output, content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=deck.zip'

    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.downloaded, 
        object=analytics.OBJECTS.deck,
        context={"deck_id": deck_id}
    )

    return response

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def create_edit_card(request, deck_id=None):
    """Create a new card or edit an existing one from the collection card template."""

    deck = Deck.objects.get(id=deck_id)
    current_collection = deck.collection
    card_color_select = widgets.Select(attrs=None, choices=Card.COLOR_CHOICES)

    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

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
    all_cards = request.GET.get('all_cards', 0)
    context = {
        "all_cards": int(all_cards),
        "deck": deck,
        "card_id": card_id if card_id else '',
        "collection": current_collection,
        "nav_collections": collection_list,
        "card_fields": card_fields,
        "card_color_select":  card_color_select.render("card_color", card_color)
    }

    return render(request, 'decks/edit_card.html', context)


@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'collection')
def edit_card_collection(request, collection_id=None):
    collection_id = Collection.objects.get(id=collection_id)
    card_id = request.GET.get('card_id', '')
    deck_id = queries.getDeckIdCard(card_id, collection_id)
    response = redirect('deckEditCard', deck_id)
    response['Location'] += '?card_id=%(c)s&deck_id=%(d)s&all_cards=%(a)s' % {'c':card_id, 'd':deck_id, 'a':1}
    return response


def log_analytics_delete(success, entity_type, entity_id, card_id, user):
    d = {'user': user}
    if success:
        log.info('Card deleted from the %(t) %(id)s' %{'t': entity_type, 'id': str(entity_id)}, extra=d)
    else:
        log.error('Card could not be deleted from the %(t) %(id)s' %{'t': entity_type, 'id': str(entity_id)}, extra=d)

    analytics.track(
        actor=user,
        verb=analytics.VERBS.deleted,
        object=analytics.OBJECTS.card,
        context={entity_type+"_id": entity_id, "card_id": card_id}
    )


@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')  
def delete_card(request, deck_id=None):
    """Deletes a card."""
    deck = Deck.objects.get(id=deck_id)
    card_id = request.GET.get('card_id', None)
    success = services.check_delete_card(card_id, [deck_id])
    log_analytics_delete(success, 'deck', deck_id, card_id, request.user)
    return redirect(deck)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'collection')
def delete_card_collection(request, collection_id=None):
    """Deletes a card."""
    deck_ids = queries.getDeckIds(collection_id)
    card_id = request.GET.get('card_id', None)
    success = services.check_delete_card(card_id, deck_ids)
    log_analytics_delete(success, 'collection', collection_id, card_id, request.user)
    return redirect('allCards', collection_id=collection_id)
