from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash.forms import CardEditForm
from harvardcards.apps.flash import services, queries, utils
from django.db import models

@require_http_methods(["POST"])
def edit2(request, card_id=None):
    """Add a new card to the deck."""
    result = {"success": False}
    card_id = request.POST.get('card_id')
    deck_id = request.POST.get('deck_id')
    deck = Deck.objects.get(id=deck_id)

    field_prefix = 'field_'
    fields = []
    errors = []

    num_nonempty_fields = 0
    for field_name, field_value in request.FILES.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                if request.FILES[field_name] and request.FILES[field_name].size > 0:
                    num_nonempty_fields = num_nonempty_fields + 1
                    if services.valid_uploaded_file(request.FILES[field_name], 'I'):
                        path = services.handle_uploaded_img_file(request.FILES[field_name], deck.id, deck.collection.id)
                        fields.append({"field_id": int(field_id), "value": path})
                    else:
                        errors.append("The uploaded image file type is not supported (must be JPG or PNG): {0}".format(request.FILES[field_name].name))


    for field_name, field_value in request.POST.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                if field_value:
                    num_nonempty_fields = num_nonempty_fields + 1
                fields.append({"field_id": int(field_id), "value": field_value})


    if num_nonempty_fields == 0:
        errors.append("All card fields are empty")

    if len(errors) > 0:
        result['error'] = errors
        return HttpResponse(json.dumps(result), mimetype="application/json")

    if card_id:
        card = Card.objects.get(id=card_id)
        services.update_card_fields(card, fields)
    else:
        card = services.add_card_to_deck(deck, fields)

    if request.POST.get('card_color') != '':
        card.color = request.POST.get('card_color')
        card.save()

    result['success'] = True
    result['data'] = {"card_id": card.id}
    result['location'] = "{0}?card_id={1}".format(deck.get_absolute_url(), card.id)

    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["POST"])
def edit(request):
    """Add a new card to the deck."""
    result = {"success":False}
    card_id = request.POST.get('card_id', '')
    deck_id = request.POST.get('deck_id', '')

    card_edit_form = CardEditForm(request.POST, request.FILES)
    if card_edit_form.is_valid():
        card_edit_form.save()
        card = card_edit_form.get_card()
        deck = card_edit_form.get_deck()
        result['success'] = True
        result['data'] = {
            "card_id": card.id,
            "card_ulr": "{0}?card_id={1}".format(deck.get_absolute_url(), card.id)
        }
    else:
        result['errors'] = card_edit_form.errors

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(["POST"])
def delete(request):
    """Deletes a card."""
    card_id = request.POST['card_id']
    result = {}
    result['success'] = services.delete_card(card_id)
    return HttpResponse(json.dumps(result), mimetype="application/json")
