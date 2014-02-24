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
    
def create(request):
    """Creates a collection."""
    collections = Collection.objects.all()

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        if collection_form.is_valid():
            collection = collection_form.save()
            return redirect(collection)
    else:
        collection_form = CollectionForm()
        
    context = {
        "collection_form": collection_form, 
        "collections": collections
    }

    return render(request, 'collections/create.html', context)

def edit(request, collection_id=None):
    """Edits a collection."""
    collections = Collection.objects.all()
    collection = Collection.objects.get(id=collection_id)

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST, instance=collection)
        if collection_form.is_valid():
            collection = collection_form.save()
            return redirect(collection)
    else:
        collection_form = CollectionForm(instance=collection)
        
    context = {
        "collection_form": collection_form, 
        "collections": collections,
        "collection": collection
    }

    return render(request, 'collections/edit.html', context)
    

def delete(request, collection_id=None):
    """Deletes a collection."""
    services.delete_collection(collection_id)
    return redirect('index')

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
            return redirect(deck)
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
