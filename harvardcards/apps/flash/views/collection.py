import datetime, base64

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist, PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm, CollectionShareForm
from harvardcards.apps.flash import forms, services, queries, utils
from harvardcards.apps.flash.services import check_role, is_superuser_or_staff


def index(request, collection_id=None):
    """Displays a set of collections to the user depending on whether 
    or not the collections are private or public and whether or not the 
    user has permission."""
    all_collections = Collection.objects.all()
    user_collection_role = Users_Collections.get_role_buckets(request.user, collections = all_collections)
    request.session['role_bucket'] = user_collection_role

    decks_by_collection = queries.getDecksByCollection()

    collection_list = []
    for collection in all_collections:
        if not collection.private or services.has_role(request, [Users_Collections.ADMINISTRATOR, 
                        Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, 
                        Users_Collections.CONTENT_DEVELOPER, Users_Collections.LEARNER], collection.id):
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
    
#should only check on collections? allow any registered user to create their own?
@login_required
def create(request):
    """Creates a collection."""

    collections = Collection.objects.all()
    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        if collection_form.is_valid():
            collection = collection_form.save()
            if request.POST.get('user_id', 0):
                user_id = int(request.POST['user_id'])
                user = User.objects.get(id=user_id)
                collection_id= Users_Collections.objects.create(user=user, collection=collection, role=Users_Collections.ADMINISTRATOR, date_joined=datetime.date.today())
                
                #update role_bucket to add admin permission to the user for this newly created collection
                services.get_or_update_role_bucket(request, collection_id.id, Users_Collections.role_map[Users_Collections.ADMINISTRATOR])
                
            response = redirect(collection)
            return response
    else:
        collection_form = CollectionForm()
        
    context = {
        "collection_form": collection_form, 
        "collections": collections
    }

    return render(request, 'collections/create.html', context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def edit(request, collection_id=None):
    """Edits a collection."""

    collections = Collection.objects.all()
    collection = Collection.objects.get(id=collection_id)

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST, instance=collection)
        if collection_form.is_valid():
            collection = collection_form.save()
            response = redirect(collection)
            response['Location'] += '?instructor=edit'
            return response
    else:
        collection_form = CollectionForm(instance=collection)
        
    context = {
        "collection_form": collection_form, 
        "collections": collections,
        "collection": collection
    }

    return render(request, 'collections/edit.html', context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def share_collection(request, collection_id=None):
    """
    Share a collection with users by creating a temporary url for authorized
    users to use in order to add themselves into the collection's authorized
    users list
    """
    print not request.POST

    collections = Collection.objects.all()
    collection = Collection.objects.get(id=collection_id)
    collection_share_form = CollectionShareForm()
    context = {
            'share_form': collection_share_form,
            'collections': collections,
            'collection': collection,
             } 

    if request.POST:
        collection_share_form = CollectionShareForm(request.POST)
        if collection_share_form.is_valid():
        
            static_url = 'collection/share/'
            generated_url = 'collection_id=%s&!!!role=%s&!!!expired_in=%s' % (collection_id, collection_share_form.cleaned_data['role'], collection_share_form.cleaned_data['expired_in'])
            context['share_link'] = static_url + base64.b64encode(generated_url)
        else:
            context['share_form'] = collection_share_form

    return render(request, 'collections/share.html', context)

@login_required
def add_user_to_shared_collection(request, parameters):
    """
    Decrypt the encrypted URL and add the user to the appropriate
    collection with the appropriate role
    """
    decrypted_info = base64.b64decode(parameters)
    collection_id, role, expire_in = decrypted_info.split('&!!!')
    collection_id = int(collection_id.split('=')[1])
    
    role = role.split('=')[1]
    expire_in = expire_in.split('=')[1]
    expire_in = datetime.datetime.strptime(expire_in,"%Y-%m-%d")
    
    current_time = datetime.datetime.now()

    if expire_in <= current_time:
        return HttpResponseBadRequest('This URL has expired.')

    collection = Collection.objects.get(id=collection_id)

    user_collection = Users_Collections(user = request.user, collection = collection, role = role, date_joined = datetime.date.today())
    user_collection.save()

    return HttpResponseRedirect("/")

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'collection')
def add_deck(request, collection_id=None):
    """Adds a deck."""

    collection = Collection.objects.get(id=collection_id)
    deck = Deck.objects.create(collection=collection, title='Untitled Deck')
    return redirect(deck)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection') 
def delete(request, collection_id=None):
    """Deletes a collection."""

    services.delete_collection(collection_id)
    response = redirect('collectionIndex')
    response['Location'] += '?instructor=edit'
    return response

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
