from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash import services, queries, utils
from django.db import models

@require_http_methods(["POST"])
def create(request):
    """Creates a new card."""
    result = {"success": False}
    deck = Deck.objects.get(id=request.POST['deck_id'])
    field_prefix = 'field_'
    card_item = []

    for field_name, field_value in request.FILES.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                path = services.handle_uploaded_img_file(request.FILES[field_name], deck.id, deck.collection.id)
                card_item.append({"field_id": int(field_id), "value": path})

    for field_name, field_value in request.POST.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                card_item.append({"field_id": int(field_id), "value": field_value})

    card = services.add_card_to_deck(deck, card_item)

    result['data'] = {"card_id": card.id}
    result['location'] = "{0}?card_id={1}".format(deck.get_absolute_url(), card.id)

    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["POST"])
def delete(request):
    """Deletes a card."""
    card_id = request.POST['card_id']
    result = {}
    result['success'] = services.delete_card(card_id)
    return HttpResponse(json.dumps(result), mimetype="application/json")
