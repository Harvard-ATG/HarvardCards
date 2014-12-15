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
    statements_json = request.POST.get('statements', '')
    statements = json.loads(statements_json)
    num_statements = len(statements)
    results = []

    for s in statements:
        verb = s.get('verb', '')
        object = s.get('object', '')
        context = s.get('context', '')
        if context == '':
            context = None
        timestamp = s.get('timestamp', '')
        if timestamp == '':
            timestamp = None

        result = {"success": False, "data": s}

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

        results.append(result)

    return HttpResponse(json.dumps({"statements": results}), mimetype="application/json")
