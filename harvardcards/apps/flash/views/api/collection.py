from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import api

def delete(request):
    """delete a collection"""
    returnValue = "false"
    if request.GET['id']:
        collection_id = request.GET['id']
        returnValue = api.deleteCollection()
    
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
    
def fields(request):
    """list the fields of a collection"""
    if 'collection_id' in request.POST:
        field_list = api.getFieldList(request.POST['collection_id'])           
        fields_json = json.dumps(field_list)
        return HttpResponse('{"success": true, "fields": %s}' % fields_json, mimetype="application/json")
        
    else:
        errorMsg = "No collection_id specified."
        for key, value in request.POST.iteritems():
            errorMsg += "<br>" + key + " => " + value
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")