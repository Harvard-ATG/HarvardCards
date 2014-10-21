import datetime, base64

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist, PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm, CollectionShareForm
from harvardcards.apps.flash import forms, services, queries, utils
from harvardcards.apps.flash.services import check_role
from harvardcards.apps.flash.queries import is_superuser_or_staff
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.apps.flash.views import card_template


def index(request, collection_id=None):
    """Displays a set of collections to the user depending on whether 
    or not the collections are private or public and whether or not the 
    user has permission."""

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)
    active_collection = None
    display_collections = collection_list
    
    if collection_id:
        try:
            cur_collection = Collection.objects.get(id=collection_id)
        except Collection.DoesNotExist:
            raise Http404
        display_collections = [c for c in collection_list if c['id'] == cur_collection.id]
        if len(display_collections) == 0:
            raise Http404
        else:
            active_collection = display_collections[0]

    context = {
        "nav_collections": collection_list,
        "display_collections": display_collections,
        "active_collection": active_collection,
        "user_collection_role": role_bucket,
    }

    return render(request, 'collections/index.html', context)
    
#should only check on collections? allow any registered user to create their own?
@login_required
def create(request):
    """Creates a collection."""

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        card_template_id = collection_form.data['card_template']
        if collection_form.is_valid():
            collection = collection_form.save()
            LTIService(request).associateCanvasCourse(collection.id)
            if request.POST.get('user_id', 0):
                user_id = int(request.POST['user_id'])
                user = User.objects.get(id=user_id)
                collection_id= Users_Collections.objects.create(user=user, collection=collection, role=Users_Collections.ADMINISTRATOR, date_joined=datetime.date.today())
                
                #update role_bucket to add admin permission to the user for this newly created collection
                services.get_or_update_role_bucket(request, collection_id.id, Users_Collections.role_map[Users_Collections.ADMINISTRATOR])
            return redirect(collection)
    else:
        initial = {'card_template': '1'}
        card_template_id = initial['card_template']
        collection_form = CollectionForm(initial=initial)
    
    # Pre-populate the "preview" of the card template
    # This view is also called via AJAX on the page.
    prev_request = HttpRequest()
    prev_request.method = 'GET'
    prev_request.GET['card_template_id'] = card_template_id
    prev_response = card_template.preview(prev_request)
    card_template_preview_html = prev_response.content
        
    context = {
        "nav_collections": collection_list,
        "active_collection": None,
        "collection_form": collection_form, 
        "card_template_preview_html": card_template_preview_html
    }

    return render(request, 'collections/create.html', context)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def edit(request, collection_id=None):
    """Edits a collection."""

    collection = Collection.objects.get(id=collection_id)

    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

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
        "nav_collections": collection_list,
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
    role_bucket = services.get_or_update_role_bucket(request)
    collection_list = queries.getCollectionList(role_bucket)

    collection = Collection.objects.get(id=collection_id)
    collection_share_form = CollectionShareForm()
    context = {
            'share_form': collection_share_form,
            'nav_collections': collection_list,
            'collection': collection,
             } 

    if request.POST:
        collection_share_form = CollectionShareForm(request.POST)
        if collection_share_form.is_valid():
            expired_in = str(collection_share_form.cleaned_data['expired_in'])

            # This creates an array of the share data (collection id and expiration data
            # for the url).  Random data is appended/prepended to "obfuscate" the url.
            # This isn't intended to be secure by any means, just make it harder to guess.
            # The assumption is that a share URL will only grant a user student-level
            # access, so they can't do any damage if they "guess" the URL. If that
            # assumption changes, then this implementation should be revisited to make it
            # more secure and tamper-proof.
            share_data = [collection_id, expired_in]
            share_data.insert(0, utils.generate_random_id(3))
            share_data.append(utils.generate_random_id(3))
            share_key = '!!'.join(share_data)

            # This pads the share key so that the base64 encoded string doesn't include
            # base64 padding, which is typically the equals sign ("=").  The equals sign
            # must be percent encoded as %3D which looks bad.  Since 3 ascii characters (8
            # bits) are encoded with 4 base64 characters (6 bits each) this should ensure
            # that the share_key is always a multiple of 3.
            if (len(share_key) % 3) > 0:
                share_key = share_key + utils.generate_random_id(3 - (len(share_key) % 3))

            secret_share_key = base64.urlsafe_b64encode(share_key.encode("ascii", "ignore"))

            context['share_form'] = collection_share_form
            context['secret_share_key'] = secret_share_key
        else:
            context['share_form'] = collection_share_form

    return render(request, 'collections/share.html', context)

@login_required
def add_user_to_shared_collection(request, secret_share_key=''):
    """
    Decrypt the encrypted URL and add the user to the appropriate
    collection with the appropriate role
    """
    decrypted_info = base64.urlsafe_b64decode(secret_share_key.encode("ascii", "ignore"))
    (random_id, collection_id, expired_in, random_id) = decrypted_info.split('!!')

    # NOTE: hard coding the role as LEARNER (i.e. student) instead of passing
    # the role via the share URL as before. That's insecure without encryption
    # and proper validation that the URL hasn't been tampered with. The main purpose
    # of the sharing functionality is to give other students access to the collection,
    # so this accomplishes that.
    role = Users_Collections.LEARNER

    if not collection_id.isdigit():
        return HttpResponseBadRequest('Invalid share URL [C]')
    if not Users_Collections.is_valid_role(role):
        return HttpResponseBadRequest('Invalid share URL [R]') 
    
    try:
        expired_in = datetime.datetime.strptime(expired_in,"%Y-%m-%d")
        current_time = datetime.datetime.now()
        if expired_in <= current_time:
            return HttpResponseBadRequest('This share URL has **expired** and is no longer valid.')
    except ValueError:
        return HttpResponseBadRequest('Invalid share URL [E]')

    if not Collection.objects.filter(id=int(collection_id)):
        return HttpResponseBadRequest('Invalid share URL [CC]')

    collection = Collection.objects.get(id=int(collection_id))
    uc_kwargs = {'user':request.user,'collection':collection,'role':role}
    if not Users_Collections.objects.filter(**uc_kwargs):
        uc_kwargs['date_joined'] = datetime.date.today()
        Users_Collections(**uc_kwargs).save()

    return HttpResponseRedirect("/")

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'collection')
def add_deck(request, collection_id=None):
    """Adds a deck."""
    deck = services.create_deck(collection_id=collection_id, deck_title='Untitled Deck')
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
