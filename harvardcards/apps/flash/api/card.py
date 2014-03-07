from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson as json

from harvardcards.apps.flash.models import Collection, Deck, Card, Cards_Fields, Field
from harvardcards.apps.flash import services, queries, utils
from django.db import models
import time
import os

def handle_uploaded_file(file):
    curr_dir = os.getcwd()
    folder_name = 'uploads'
    parent_dir = os.path.abspath(os.path.join(curr_dir, 'harvardcards', 'apps', 'flash'))
    parent_dir1 = os.path.abspath(os.path.join(parent_dir, folder_name))
    if not os.path.exists(parent_dir1):
        os.chdir(parent_dir)
        os.mkdir(folder_name)
        os.chdir(curr_dir)
    dirfmt = "%4d-%02d-%02d"
    dir_name = dirfmt % time.localtime()[0:3]
    path = os.path.abspath(os.path.join(parent_dir1, dir_name))
    if not os.path.exists(path):
        os.chdir(parent_dir1)
        os.mkdir(dir_name)
        os.chdir(curr_dir)
    file_name = file.name
    full_path = os.path.join(path, file_name)
    dest = open(os.path.join(path, file_name), 'wb+')
    if file.multiple_chunks:
        for c in file.chunks():
            dest.write(c)
    else:
        dest.write(file.read())
    dest.close()
    return os.path.join('\media', dir_name, file_name)

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
                path = handle_uploaded_file(request.FILES[field_name])
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
