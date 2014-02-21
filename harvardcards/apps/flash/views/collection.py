from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import forms, services, queries, utils

def index(request, collection_id=None):
    """main landing page"""
    collections = Collection.objects.all()
    user_collection_role = Users_Collections.get_role_buckets(request.user, collections)

    decks_by_collection = queries.getDecksByCollection()

    collection_list = []
    for collection in collections:
        collection_decks = []
        if decks_by_collection.get(collection.id, 0):
            for deck in decks_by_collection[collection.id]:
                collection_decks.append({
                    'id': deck.id,
                    'title': deck.title,
                    'num_cards': deck.cards.count()
                })
            collection_list.append({
                'id': collection.id,
                'title':collection.title,
                'decks': collection_decks
            })
        else:
            collection_list.append({
                'id': collection.id,
                'title':collection.title,
                'decks': []
            })

    context = {
        "collections": collection_list,
        "user_collection_role": user_collection_role
    }

    if collection_id:
        current_collection = collections.get(id=collection_id)
        curr_collection = filter(lambda x: x['id']==current_collection.id, collection_list)
        context = {
        "collections": collection_list,
        "user_collection_role": user_collection_role,
        "collection": curr_collection[0]
        }
        return render(request, 'current_collection_view.html', context)
    else:
        return render(request, 'collection_index.html', context)
    
def create(request, collection_id=None):
    """create a collection"""
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
            #
            # # create the formset from the base fieldform
            # #FieldFormSet = formset_factory(FieldForm)
            # # decode json
            # data = json.loads(request.POST['field_data'])
            # #return HttpResponse(repr(data))
            #
            # # is it an edit?
            # # get all ids from data
            # editList = []
            # for d in data:
            #     if 'id' in d:
            #         editList.append(d['id']);
            # if len(editList):
            #     # then run through all ids in the db
            #     # if they are not in edit list, delete them
            #     existingFields = Field.objects.filter(collection=collection.id)
            #     for ef in existingFields:
            #         if ef.id not in editList:
            #             ef.delete()
            #
            #
            # # run through field_data
            # for d in data:
            #     if 'id' in d:
            #         field = Field.objects.get(id=d['id'])
            #         fieldForm = FieldForm(d, instance=field)
            #     else:
            #         fieldForm = FieldForm(d)
            #
            #     f = fieldForm.save(commit=False)
            #     # this is how relationships have to be done -- forms cannot handle this
            #     # so you have to do it directly at the model
            #     f.collection = collection
            #     f.save()
                                
            object = Collection.objects.get(id = collection.id)
            return redirect(object)
        else:
            return render(index)
    
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

def upload_deck(request, collection_id=None):
    '''
    Uploads a deck of cards from an excel spreadsheet.
    '''
    collections = Collection.objects.all().prefetch_related('deck_set')
    collection = Collection.objects.get(id=collection_id)

    if request.method == 'POST':
        form = forms.DeckImportForm(request.POST, request.FILES)
        if form.is_valid():
            deck = services.handle_uploaded_deck_file(collection_id, form.cleaned_data['deck_title'], request.FILES['file'])
            return redirect('deckIndex', deck.id)
    else:
        form = forms.DeckImportForm()

    context = {
        "form": form, 
        "collection": collection,
        "collections": collections
    }

    return render(request, 'collections/upload_deck.html', context)

def download_template(request, collection_id=None):
    '''
    Downloads an excel spreadsheet that may be used as a template for uploading
    a deck of cards.
    '''
    collection = Collection.objects.get(id=collection_id)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=flashcards_template.xls'

    file_output = utils.create_deck_template_file(collection.card_template)
    response.write(file_output)

    return response
