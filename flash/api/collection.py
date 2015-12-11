from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import redirect

from flash.models import Collection, Users_Collections
from flash import queries
from flash.decorators import check_role

import json

@require_http_methods(["POST"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def delete(request, collection_id=None):
    """Delete a collection"""

    result = {"success": False}
    if collection_id is not None:
        result['success'] = services.delete_collection(collection_id)
        redirect_response = redirect('index')
        result['location'] = redirect_response['Location']
    return HttpResponse(json.dumps(result), mimetype="application/json")

@require_http_methods(["GET"])
@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def fields(request, collection_id=None):
    """list the fields of a collection"""

    result = {"success": False, "fields": []}
    if collection_id is not None:
        result['fields'] = queries.getFieldList(collection_id)
        result['success'] = True;
    return HttpResponse(json.dumps(result), mimetype="application/json")
