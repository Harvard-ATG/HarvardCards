from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist
from django.contrib.auth.models import User

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm
from harvardcards.apps.flash import forms, services, queries, utils
import datetime

def index(request, collection_id=None):
    """Displays a set of collections."""
    all_collections = Collection.objects.all()
    user_collection_role = Users_Collections.get_role_buckets(request.user, all_collections)
    decks_by_collection = queries.getDecksByCollection()

    collection_list = []
    for collection in all_collections:
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

    if collection_id:
        cur_collection = all_collections.get(id=collection_id)
        display_collections = [c for c in collection_list if c['id'] == cur_collection.id]
        display_collection = display_collections[0]
    else:
        display_collections = collection_list
        display_collection = None

    context = {
        "collections": collection_list,
        "display_collections": display_collections,
        "display_collection": display_collection,
        "user_collection_role": user_collection_role,
    }

    return render(request, 'collections/index.html', context)
    
def create(request):
    """Creates a collection."""
    collections = Collection.objects.all()
    if request.method == 'POST':
        user_id = int(request.POST['user_id'])
        user = User.objects.get(id=user_id)
        collection_form = CollectionForm(request.POST)
        if collection_form.is_valid():
            collection = collection_form.save()
            Users_Collections.objects.create(user=user, collection=collection, role='A', date_joined=datetime.date.today())

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
            if 'file' in request.FILES:
                deck = services.handle_uploaded_deck_file(collection_id, form.cleaned_data['deck_title'], request.FILES['file'])
            else:
                deck = Deck.objects.create(collection=collection, title=form.cleaned_data['deck_title'])
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
