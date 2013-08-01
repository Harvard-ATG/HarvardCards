from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm

def index(request):
    #return HttpResponse("Hello Werld. This is the HarvardCards Index.")
    collections = Collection.objects.all()
    # can get decks in the template by using collection.deck_set.all
    
    return render(request, 'index.html', {"collections": collections})
    
def create(request, collection_id=None):
    # is it a post?
    message = '';
    if request.method == 'POST':
        #for key in request.POST:
        #    value = request.POST[key]
        #    message += "{0} => {1}<br>".format(key, value)
        #return HttpResponse(message)
        
        if 'collection_id' in request.POST:
            collection = Collection.objects.get(id=request.POST['collection_id'])
            collectionForm = CollectionForm(request.POST, instance=collection)
            
        else:
            collectionForm = CollectionForm(request.POST)
        
        if collectionForm.is_valid():
            collection = collectionForm.save()

            # create the formset from the base fieldform
            #FieldFormSet = formset_factory(FieldForm)
            # decode json
            data = json.loads(request.POST['field_data'])            
            #return HttpResponse(repr(data))
            
            # is it an edit?
            # get all ids from data
            editList = []
            for d in data:
                if 'id' in d:
                    editList.append(d['id']);
            if len(editList):
                # then run through all ids in the db
                # if they are not in edit list, delete them
                existingFields = Field.objects.filter(collection=collection.id)
                for ef in existingFields:
                    if ef.id not in editList:
                        ef.delete()
                

            # run through field_data
            for d in data:
                if 'id' in d:
                    field = Field.objects.get(id=d['id'])
                    fieldForm = FieldForm(d, instance=field)
                else:
                    fieldForm = FieldForm(d)
                
                f = fieldForm.save(commit=False)
                # this is how relationships have to be done -- forms cannot handle this
                # so you have to do it directly at the model
                f.collection = collection
                f.save()
                
                

            return redirect(index)
        else:
            return render(request, 'collections/create.html')
    
    # is it an edit?
    elif collection_id:
        collection = Collection.objects.get(id=collection_id)
        fields = collection.field_set.all().order_by('sort_order')
        if collection:
            return render(request, 'collections/create.html', {"collection": collection, "fields": fields})
        else:
            raise ViewDoesNotExist("Course does not exist.")
    
            
    else:
        return render(request, 'collections/create.html')

def delete(request):
    returnValue = "false"
    if request.GET['id']:
        collection_id = request.GET['id']
        Collection.objects.filter(id=collection_id).delete()
        if not Collection.objects.filter(id=collection_id):
            returnValue = "true"
    
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
    