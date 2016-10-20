from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import redirect

from flash.models import Collection, Deck, Users_Collections
from flash.forms import DeckForm
from flash.decorators import check_role
from flash import queries 
import json

@require_http_methods(["POST"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def delete(request):
    """Delete a deck"""
    deck_id = request.POST['deck_id']

    result = {"success": False}
    if deck_id is None:
        result['error'] = "Missing deck_id parameter"
    elif not Deck.objects.filter(id=deck_id).exists():
        result['error'] = "Deck not found"
    else:
        collection_id = queries.getDeckCollectionId(deck_id)
        result['success'] = services.delete_deck(deck_id)
        redirect_response = redirect('collectionIndex', collection_id)
        result['location'] = redirect_response['Location']
    return HttpResponse(json.dumps(result), content_type="application/json")

@require_http_methods(["POST"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'deck')
def rename(request):
    """Rename a deck"""
    deck_id = request.POST['deck_id']

    result = {"success": False}
    if deck_id is None:
        result['error'] = "Missing deck_id parameter"
    elif not Deck.objects.filter(id=deck_id).exists():
        result['error'] = "Deck not found"
    else:
        deck = Deck.objects.get(id=deck_id)
        deck_form = DeckForm(request.POST, instance=deck)
        result['success'] = deck_form.is_valid()
        if deck_form.is_valid():
            deck = deck_form.save()
        else:
            result['errors'] = {'title': deck_form['title'].errors}
    return HttpResponse(json.dumps(result), content_type="application/json")
