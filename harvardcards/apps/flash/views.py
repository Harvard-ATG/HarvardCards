from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from models import Collection, Deck
from forms import CollectionForm, FieldForm

def index(request):
    #return HttpResponse("Hello Werld. This is the HarvardCards Index.")
    collections = Collection.objects.all()
    # can get decks in the template by using collection.deck_set.all
    
    return render(request, 'index.html', {"collections": collections})
    
def splash(request):
    return render(request, 'splash.html')
    
def main(request):
    return render(request, 'main.html')
    
def create(request):
    # this is only POSTed when creating -- editing will be done on the fly
    if request.method == 'POST':
        collectionForm = CollectionForm(request.POST)
        
        if collectionForm.is_valid():
            collection = collectionForm.save()
        
            # create the formset from the base fieldform
            FieldFormSet = formset_factory(FieldForm)
            # decode json
            data = json.loads(request.POST['field_data'])
            
            formset = FieldFormSet(initial=data)
        
            # run through the formset to save each one
            for form in formset:
                f = form.save(commit=False)
                f.collection = collection
                f.save()
        else:
            return render(request, 'collections/create.html')
            
        return redirect(index)
    else:
        return render(request, 'collections/create.html')

def delete(request):
    returnValue = "false"
    message = '';
    for key,value in request.GET.items():
        message += key + " => " + value + "<br>\n"
    if request.GET['id']:
        collection_id = request.GET['id']
        Collection.objects.filter(id=collection_id).delete()
        if not Collection.objects.filter(id=collection_id):
            returnValue = "true"
    
#    return HttpResponse(message);
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
