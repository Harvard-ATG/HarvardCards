from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field, Users_Collections
from harvardcards.apps.flash.forms import CardEditForm
from harvardcards.apps.flash import services, queries, utils
from harvardcards.apps.flash.services import check_role
from django.db import models

import urllib2
from django.utils.datastructures import MultiValueDict
from django.core.files import File
from cStringIO import StringIO
from PIL import Image, ImageFile    

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
    
    # attempted to validate and save the form data
    file_url = dict(request.POST).get('image_url', '')
    file_url = file_url[0] if file_url else None

    if file_url:
        inStream = urllib2.urlopen(file_url)

        parser = ImageFile.Parser()
        while True:
            s = inStream.read(1024)
            if not s:
                break
            parser.feed(s)

        inImage = parser.close()
        # convert to RGB to avoid error with png and tiffs
        #if inImage.mode != "RGB":
        #    inImage = inImage.convert("RGB")

        img_temp = StringIO()
        inImage.save(img_temp, 'PNG')
        img_temp.seek(0)
        file_object = File(img_temp, 'img_temp.png')
        uploaded_file = MultiValueDict({'field_3': [file_object]})
    else:
        uploaded_file = request.FILES
    
    card_edit_form = CardEditForm(request.POST, uploaded_file, card_fields=card_fields)
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
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def delete(request):
    """Deletes a card."""
    card_id = request.POST['card_id']
    deck_id = request.POST['deck_id']

    result = {}
    result['success'] = services.delete_card(card_id)
    return HttpResponse(json.dumps(result), mimetype="application/json")
