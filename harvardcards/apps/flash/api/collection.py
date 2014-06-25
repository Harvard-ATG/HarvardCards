from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import services, queries

@require_http_methods(["POST"])
def delete(request, collection_id=None):
    """Delete a collection"""

    # ROLE CHECK -- make sure user has permission
    services.check_role_collection(user=request.user, role="A", collection_id=collection_id, raise_exception=True)

    result = {"success": False}
    if collection_id is not None:
        result['success'] = services.delete_collection(collection_id)
        redirect_response = redirect('index')
        result['location'] = redirect_response['Location']
    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["GET"])
def fields(request, collection_id=None):
    """list the fields of a collection"""

    # ROLE CHECK -- make sure user has permission
    services.check_role_collection(user=request.user, role="A", collection_id=collection_id, raise_exception=True)

    result = {"success": False, "fields": []}
    if collection_id is not None:
        result['fields'] = queries.getFieldList(collection_id)
        result['success'] = True;
    return HttpResponse(json.dumps(result), mimetype="application/json")
