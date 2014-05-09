from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash import services, queries, utils
from django.db import models

@require_http_methods(["POST"])
def create(request, deck_id = None):
    """Add a new card to the deck."""
    result = {"success": False}
    deck = Deck.objects.get(id=deck_id)


    field_prefix = 'field_'
    fields = []

    num_fields = 0
    for field_name, field_value in request.FILES.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                if request.FILES[field_name].size > 0:
                    if request.FILES[field_name]:
                        if not services.valid_uploaded_file(request.FILES[field_name], 'I'):
                            result['error'] = "The uploaded image file type is not supported."
                            return HttpResponse(json.dumps(result), mimetype="application/json")
                        num_fields = num_fields + 1
                        path = services.handle_uploaded_img_file(request.FILES[field_name], deck.id, deck.collection.id)
                        fields.append({"field_id": int(field_id), "value": path})

    for field_name, field_value in request.POST.items():
        if field_name.startswith(field_prefix):
            field_id = field_name.replace(field_prefix, '')
            if field_id.isdigit():
                if field_value:
                    num_fields = num_fields + 1
                    fields.append({"field_id": int(field_id), "value": field_value})


    if num_fields==0:
        result['error'] = "All Card Fields are Empty."
        return HttpResponse(json.dumps(result), mimetype="application/json")


    if request.POST.get('card_id', '') == '':
        card = services.add_card_to_deck(deck, fields)
    else:
        card = Card.objects.get(id=request.POST.get('card_id'))
        services.update_card_fields(card, fields)

    if request.POST.get('card_color') != '':
        card.color = request.POST.get('card_color')
        card.save()
    result['success'] = True

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
