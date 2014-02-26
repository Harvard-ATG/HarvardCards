from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from harvardcards.apps.flash.models import CardTemplate

@require_GET
def preview(request):
    '''
    Returns a snippet of HTML that shows a "preview" of the card template.
    '''
    card_template_id = request.GET['card_template_id']
    card_template = CardTemplate.objects.get(id=card_template_id)
    card_template_fields = {'show':[],'reveal':[]}
    for field in card_template.fields.all():
        if field.display:
            bucket = 'show'
        else:
            bucket = 'reveal'
        card_template_fields[bucket].append({
            'id': field.id,
            'type': field.field_type,
            'label': field.label,
            'show_label': field.show_label,
        })

    context = {
        "card_template_title": card_template.title,
        "card_template_description": card_template.description,
        "card_template_fields": card_template_fields
    }

    return render(request, "card_template_preview.html", context)
