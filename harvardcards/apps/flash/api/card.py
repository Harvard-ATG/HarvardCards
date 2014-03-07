from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash import services, queries, utils
from django.db import models




@require_http_methods(["POST"])
def create(request):
    """Creates a new card."""
    deck = Deck.objects.get(id=request.POST['deck_id'])
    errorMsg = ''
    field_prefix = 'field_'
    fields = []
    for field_name, field_value in request.FILES.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                path = services.handle_uploaded_img_file(request.FILES[field_name], deck.id, deck.collection.id)
                fields.append({"field_id": int(field_id), "value": path})

    for field_name, field_value in request.POST.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                fields.append({"field_id": int(field_id), "value": field_value})

    cards = [fields]
    services.add_cards_to_deck(deck, cards)

    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")

@require_http_methods(["POST"])
def delete(request, card_id=None):
    """Deletes a card."""
    success = services.delete_card(card_id)
    return HttpResponse('{"success": %s}' % success, mimetype="application/json")
