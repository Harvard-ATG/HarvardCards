from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

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
    
def create(request, collection_id=None):
    # is it an edit?
    if collection_id:
        collection = Collection.objects.get(id=collection_id)
        fields = collection.field_set.all().order_by('sort_order')
        if collection:
            return render(request, 'collections/create.html', {"collection": collection, "fields": fields})
        else:
            raise ViewDoesNotExist("Course does not exist.")
    # is it a new post?
    elif request.method == 'POST':
        collectionForm = CollectionForm(request.POST)
        
        if collectionForm.is_valid():
            collection = collectionForm.save()
        
            # create the formset from the base fieldform
            #FieldFormSet = formset_factory(FieldForm)
            # decode json
            data = json.loads(request.POST['field_data'])            
            
            # run through field_data
            for d in data:
                fieldForm = FieldForm(d)
                f = fieldForm.save(commit=False) 
                # this is how relationships have to be done -- forms cannot handle this
                # so you have to do it directly at the model
                f.collection = collection
                f.save()

            return redirect(index)
        else:
            return render(request, 'collections/create.html')
            
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
