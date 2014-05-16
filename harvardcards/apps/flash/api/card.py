from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash.forms import CardEditForm
from harvardcards.apps.flash import services, queries, utils
from django.db import models

@require_http_methods(["POST"])
def edit(request):
    """Add/edit card."""
    result = {"success":False}
    card_id = request.POST.get('card_id', '')
    deck_id = request.POST.get('deck_id', '')

    # fetch the fields being edited; new cards must be created from the card template
    if card_id == '':
        deck = Deck.objects.get(id=deck_id)
        card_fields = deck.collection.card_template.fields.all()
    else:
        card = Card.objects.get(id=card_id)
        card_fields = [cfield.field for cfield in card.cards_fields_set.all()]

    # attempted to validate and save the form data
    card_edit_form = CardEditForm(request.POST, request.FILES, card_fields=card_fields)
    if card_edit_form.is_valid():
        card_edit_form.save()
        card = card_edit_form.get_card()
        deck = card_edit_form.get_deck()
        result['success'] = True
        result['data'] = {
            "card_id": card.id,
            "card_url": "{0}?card_id={1}".format(deck.get_absolute_url(), card.id)
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
