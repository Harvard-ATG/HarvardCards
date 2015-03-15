from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field, Users_Collections
from harvardcards.apps.flash.forms import CardEditForm
from harvardcards.apps.flash import services, queries, utils, analytics
from harvardcards.apps.flash.decorators import check_role

import json
import urllib2


@require_http_methods(["POST"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
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

    for k, v in request.POST.iteritems():
        if k.endswith('_image_url') and v:
            field_name = k.replace('_image_url', '')
            request.FILES[field_name] = services.fetch_image_from_url(v)

    # attempted to validate and save the form data
    card_edit_form = CardEditForm(request.POST, request.FILES, card_fields=card_fields)
    if card_edit_form.is_valid():
        card_edit_form.save()
        card = card_edit_form.get_card()
        deck = card_edit_form.get_deck()
        result['success'] = True
        is_all_cards = request.GET.get('is_all_cards', 0)
        if int(is_all_cards):
            base_url = deck.collection.get_all_cards_url()
        else:
            base_url = deck.get_absolute_url()

        result['data'] = {
            "card_id": card.id,
            "card_url": "{0}?card_id={1}".format(base_url, card.id)
        }
    else:
        card_edit_form.get_card().delete()
        result['errors'] = card_edit_form.errors

    analytics.track(
        actor=request.user,
        verb=analytics.VERBS.modified,
        object=analytics.OBJECTS.card,
        context={"deck_id": deck_id, "card_id": card_id},
    )

    return HttpResponse(json.dumps(result), mimetype="application/json")


@require_http_methods(["POST"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def delete(request):
    """Deletes a card."""
    card_id = request.POST['card_id']
    deck_id = request.POST['deck_id']

    result = {}
    result['success'] = services.delete_card(card_id)
    return HttpResponse(json.dumps(result), mimetype="application/json")
