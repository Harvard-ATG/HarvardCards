import datetime, base64
import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist, PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.forms.formsets import formset_factory

from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field, CardTemplate
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm, CollectionShareForm
from harvardcards.apps.flash.decorators import check_role
from harvardcards.apps.flash.lti_service import LTIService
from harvardcards.apps.flash.views import card_template
from harvardcards.apps.flash import services, queries, utils, analytics

import logging
log = logging.getLogger(__name__)

def index(request, collection_id=None):
    """Displays a set of collections to the user depending on whether 
    or not the collections are private or public and whether or not the 
    user has permission."""

    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)
    copy_collections = queries.getCopyCollectionList(request.user)
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
        "copy_collections": copy_collections,
        "active_collection": active_collection,
        "user_collection_role": role_bucket,
    }

    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.viewed, 
        object=analytics.OBJECTS.collection,
        context={"collection_id": collection_id}
    )

    return render(request, 'collections/index.html', context)

@login_required
def custom_create(request):
    """
    Creates a collection with custom template.
    """
    upload_error = ''
    course_name = ''
    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)
    if request.method == 'POST':
        d = {'user': request.user}
        log.info('The user is uploading a custom deck.', extra=d)

        course_name = request.POST.get('course', '')
        if course_name == '' or 'file' not in request.FILES:
            if course_name == '' and 'file' not in request.FILES:
                upload_error = "Course name needed. No file selected."
            elif course_name != '' and 'file' not in request.FILES:
                upload_error = 'No file selected'
            else:
                upload_error = 'Course name needed.'
        else:
            try:
                deck = services.handle_custom_file(request.FILES['file'], course_name, request.user)
                log.info('Custom deck %(d)s successfully added to the new collection %(c)s.'
                         %{'c': str(deck.collection.id), 'd':str(deck.id)}, extra=d)
                return redirect(deck)
            except Exception, e:
                    upload_error = str(e)
        msg = 'The following error occurred when the user tried uploading a deck: '
        log.error(msg + upload_error , extra=d)

    context = {
        "nav_collections": collection_list,
        "active_collection": None,
        'upload_error': upload_error,
        "course_name": course_name or ''
    }

    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.created, 
        object=analytics.OBJECTS.collection,
        context={"custom": True}
    )

    return render(request, 'collections/custom.html', context)

#should only check on collections? allow any registered user to create their own?
@login_required
def create(request):
    """Creates a collection."""

    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        card_template_id = collection_form.data['card_template']
        if collection_form.is_valid():
            collection = collection_form.save()
            LTIService(request).associateCanvasCourse(collection.id)
            services.add_user_to_collection(user=request.user, collection=collection, role=Users_Collections.ADMINISTRATOR)
            #update role_bucket to add admin permission to the user for this newly created collection
            services.get_or_update_role_bucket(request, collection.id, Users_Collections.role_map[Users_Collections.ADMINISTRATOR])
            log.info('Collection %s created.' %collection.id, extra={'user': request.user})
            analytics.track(
                actor=request.user, 
                verb=analytics.VERBS.created, 
                object=analytics.OBJECTS.collection,
                context={"custom": False}
            )
            return redirect(collection)
    else:
        rel_templates = CardTemplate.objects.filter(Q(owner__isnull=True) | Q(owner=request.user))
        initial = {'card_template': '1'}
        card_template_id = initial['card_template']
        collection_form = CollectionForm(query_set=rel_templates,initial=initial)


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
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

    if request.method == 'POST':
        collection_form = CollectionForm(request.POST, instance=collection)
        if collection_form.is_valid():
            collection = collection_form.save()
            response = redirect(collection)
            response['Location'] += '?instructor=edit'
            analytics.track(
                actor=request.user, 
                verb=analytics.VERBS.modified, 
                object=analytics.OBJECTS.collection,
                context={"collection_id": collection_id}
            )
            return response
    else:
        collection_form = CollectionForm(instance=collection)

    collection_decks = []
    for c in collection_list:
        if c['id'] == collection.id:
            collection_decks = c['decks']
            break
        
    context = {
        "collection_form": collection_form, 
        "nav_collections": collection_list,
        "collection": collection,
        "collection_decks": collection_decks,
    }

    return render(request, 'collections/edit.html', context)

@login_required
@require_http_methods(["POST"])
def copy_collection(request):
    collection_id = request.POST.get('collection_id', '')
    if collection_id == '':
        raise Http404

    has_perm_to_copy = queries.can_copy_collection(request.user, collection_id)
    if not has_perm_to_copy:
         raise PermissionDenied()

    new_collection = services.copy_collection(request.user, collection_id)

    services.add_user_to_collection(user=request.user, collection=new_collection, role=Users_Collections.ADMINISTRATOR)
    LTIService(request).associateCanvasCourse(new_collection.id)

    return redirect(new_collection)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection')
def share_collection(request, collection_id=None):
    """
    Share a collection with users by creating a temporary url for authorized
    users to use in order to add themselves into the collection's authorized
    users list
    """
    role_bucket = services.get_or_update_role_bucket(request)
    canvas_course_collections = LTIService(request).getCourseCollections()
    collection_list = queries.getCollectionList(role_bucket, collection_ids=canvas_course_collections)

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
            log.info('URL generated to share collection %s.' %collection_id, extra={'user': request.user})
            analytics.track(
                actor=request.user, 
                verb=analytics.VERBS.shared, 
                object=analytics.OBJECTS.collection,
                context={"collection_id": collection_id}
            )
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
    uc_kwargs = {'user':request.user,'collection':collection,'role':Users_Collections.OBSERVER}
    if not Users_Collections.objects.exclude(**uc_kwargs):
        uc_kwargs['role'] = role
        uc_kwargs['date_joined'] = datetime.date.today()
        Users_Collections(**uc_kwargs).save()
    log.info('User added to the collection %s as a learner.' %collection_id, extra={'user': request.user})
    return HttpResponseRedirect("/")

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR, Users_Collections.TEACHING_ASSISTANT, Users_Collections.CONTENT_DEVELOPER], 'collection')
def add_deck(request, collection_id=None):
    """Adds a deck."""
    deck = services.create_deck(collection_id=collection_id, deck_title='Untitled Deck')
    log.info('Deck %(d)s added to the collection %(c)s.' %{'d': deck.id, 'c': str(collection_id)}, extra={'user': request.user})
    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.created, 
        object=analytics.OBJECTS.deck,
        context={"collection_id": collection_id, "deck_id": deck.id}
    )
    return redirect(deck)

@check_role([Users_Collections.ADMINISTRATOR, Users_Collections.INSTRUCTOR], 'collection') 
def delete(request, collection_id=None):
    """Deletes a collection."""

    services.delete_collection(collection_id)
    response = redirect('collectionIndex')
    response['Location'] += '?instructor=edit'
    log.info('Collection %(c)s deleted.' %{'c': str(collection_id)}, extra={'user': request.user})
    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.deleted, 
        object=analytics.OBJECTS.collection,
        context={"collection_id": collection_id}
    )
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
    log.info('Template for the collection %(c)s downloaded by the user.'
            %{'c': str(collection_id)}, extra={'user': request.user})

    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.downloaded, 
        object=analytics.OBJECTS.template,
        context={"collection_id": collection_id, "custom": False}
    )

    return response

def download_custom_template(request, collection_id=None):
    '''
    Downloads an excel spreadsheet that may be used as a template for uploading
    a deck of cards.
    '''

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=flashcards_template.xls'

    file_output = utils.create_custom_template_file()
    response.write(file_output)
    log.info('Custom template downloaded.', extra={'user': request.user})

    analytics.track(
        actor=request.user, 
        verb=analytics.VERBS.downloaded, 
        object=analytics.OBJECTS.template,
        context={"collection_id": collection_id, "custom": True}
    )

    return response
