from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist
from django.views.decorators.http import require_http_methods

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import services, queries

@require_http_methods(["POST"])
def delete(request, collection_id=None):
    """Delete a collection"""
    result = {"success": False}
    if collection_id is not None:
        result['success'] = services.delete_collection(collection_id)
        redirect_response = redirect('index')
        result['location'] = redirect_response['Location']
    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["GET"])
def fields(request):
    """list the fields of a collection"""
    if 'collection_id' in request.POST:
        field_list = queries.getFieldList(request.POST['collection_id'])           
        fields_json = json.dumps(field_list)
        return HttpResponse('{"success": true, "fields": %s}' % fields_json, mimetype="application/json")
        
    else:
        errorMsg = "No collection_id specified."
        for key, value in request.POST.iteritems():
            errorMsg += "<br>" + key + " => " + value
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
