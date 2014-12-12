from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

from harvardcards.apps.flash import analytics

import logging
log = logging.getLogger(__name__)

@login_required
@require_http_methods(["POST"])
def track(request):
    actor = request.user
    verb = request.POST.get('verb', '')
    object = request.POST.get('object', '')
    context = request.POST.get('context', '')

    if context == '':
        context = None
    else:
        context = json.loads(context)

    timestamp = request.POST.get('timestamp', '')
    if timestamp == '':
        timestamp = None

    result = {"success": False, "data": {}}

    if verb != '' and object != '':
        statement = analytics.track(
            actor=actor,
            verb=verb,
            object=object,
            timestamp=timestamp,
            context=context,
        )
        result['success'] = True
        result['data'] = statement.as_dict()

    return HttpResponse(json.dumps(result), mimetype="application/json")
