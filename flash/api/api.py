from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json

def root(request):
    result = {"name": "Harvard Cards", "version": "1.0"}
    return HttpResponse(json.dumps(result), content_type="application/json")
