"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""
import urllib2
import os
import shutil
import datetime
import zipfile
import tempfile

from PIL import Image, ImageFile
from cStringIO import StringIO
from mutagen.mp3 import MP3
from datetime import date

from django.db import transaction
from django.db.models import Avg, Max, Min
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File

from flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields, Field, Users_Collections, CardTemplate, CardTemplates_Fields, Clone, Cloned
from flash.media_store_service import MediaStoreService
from flash import utils
from flash import queries


def delete_collection(collection_id):
    """Deletes a collection and returns true on success, false otherwise."""
    Collection.objects.get(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    return False

def delete_deck(deck_id):
    """Deletes a deck and returns true on success, false otherwise."""
    deck = Deck.objects.get(id=deck_id)
    deck.delete()
    if not Deck.objects.filter(id=deck_id):
        return True
    return False

def delete_card(card_id):
    """Deletes a card and returns true on success, false otherwise."""
    Card.objects.get(id=card_id).delete()
    if not Card.objects.filter(id=card_id):
        return True
    return False

def check_delete_card(card_id, deck_ids):
    """Checks if card is in one of the decks and deletes it"""
    success = False
    for deck_id in deck_ids:
        if success:
            break
        if queries.isCardInDeck(card_id, deck_id):
            success = delete_card(card_id)
    return success

def valid_image_file_type(file_path):
    """Returns true if the given file is a valid image type."""
    valid_types = ['rgb', 'gif', 'png', 'bmp', 'gif', 'jpeg']
    try:
        img = Image.open(file_path)
        img_type = (img.format).lower()
        if img_type not in valid_types:
            return [False, "Image must be one of: %s" % ", ".join(valid_types)]
    except Exception as e:
        return [False, str(e)]
    return [True, '']

def valid_audio_file_type(file_path):
    """Returns true if the given file is a valid audio type."""
    try:
        audio = MP3(file_path)
    except Exception as e:
        return [False, str(e)]
    return [True, '']

def handle_uploaded_media_file(file, file_type=None):
    """Handles an uploaded file and returns the path to the file object."""
    store_service = MediaStoreService(file=file, file_type=file_type)
    store_service.save()
    return store_service.storeFileName()

def fetch_image_from_url(file_url):
    """Returns an UploadedFile object after retrieving the file at the given URL."""
    inStream = urllib2.urlopen(file_url)

    parser = ImageFile.Parser()
    file_size = 0
    max_file_size = 20 * 1024 * 1024 # 20 megabytes
    read_size = 1024
    while True:
        s = inStream.read(read_size)
        file_size += len(s)
        if not s:
            break
        if file_size > max_file_size:
            raise Exception("file size exceeded max size: %s bytes" % max_file_size)
        parser.feed(s)

    inImage = parser.close()
    # convert to RGB to avoid error with png and tiffs
    #if inImage.mode != "RGB":
    #    inImage = inImage.convert("RGB")

    img_temp = StringIO()
    inImage.save(img_temp, 'PNG')
    img_temp.seek(0)

    file_object = File(img_temp, 'img_temp.png')
    uploaded_file = UploadedFile(file=file_object, name=file_object.name, content_type='image/png', size=file_size, charset=None)

    return uploaded_file

def fetch_audio_from_url(file_url):
    """Returns an UploadedFile object after retrieving the file at the given URL."""
    inStream = urllib2.urlopen(file_url)
    file_object = tempfile.NamedTemporaryFile(mode='r+', suffix='.mp3')
    file_size = 0
    max_file_size = 10 * 1024 * 1024 # 10 megabytes
    read_size = 1024

    while True:
        s = inStream.read(read_size)
        file_size += len(s)
        if not s:
            break
        if file_size > max_file_size:
            raise Exception("file size exceeded max size: %s bytes" % max_file_size)
        file_object.write(s)

    file_object.seek(0)

    uploaded_file = UploadedFile(file=file_object, name=file_object.name, content_type='audio/mp3', size=file_size, charset=None)

    return uploaded_file

def create_zip_deck_file(deck):
    """Creates a zipped file containing the contents of the deck (XLS and media objects."""

    # create the string buffer to hold the contents of the zip file
    s = StringIO()

    # create the zipfile object
    zfile = zipfile.ZipFile(s, "w")

    # write the deck XLS file to the zip
    deck_file_output = utils.create_deck_file(deck.id)
    temp_dirpath = tempfile.mkdtemp()
    temp_filepath = os.path.join(temp_dirpath, "deck.xls")
    deck_file_output.save(temp_filepath)
    zfile.write(temp_filepath, arcname=os.path.split(temp_filepath)[1])
    shutil.rmtree(temp_dirpath) # must delete temp dir when we're done

    # lookup the unique field values in the deck of cards,
    # where the field values are the media object names
    card_list = queries.getDeckCardsList(deck.id)
    field_set = set()
    for c in card_list:
        for f in c['fields']:
            if f['type'] not in ('T', 'M'):
                field_set.add(f['value'])

    # add each media object ot the zip file
    for file_name in field_set:
        file_contents = MediaStoreService.readFileContents(file_name)
        if file_contents is not None:
            zfile.writestr(file_name, file_contents)

    zfile.close()

    return s.getvalue()

def extract_from_zip(uploaded_file):
    """
    Checks for valid spreadsheet file in the zipped folder.
    Returns the spreadsheet, zip file and relevant file names.
    """
    zfile = zipfile.ZipFile(uploaded_file, 'r')
    file_names = zfile.namelist()

    # This filters the __MACOSX/ folder entries from the zip file, which
    # should be ignored for the upload (only relevant for MAC-created zip files).
    file_names = [file_name for file_name in file_names if "__MACOSX" not in file_name]

    # Make sure file names always returned in sorted order
    file_names.sort()

    excel_files = filter(lambda f: os.path.splitext(f)[1][1:].strip().lower() in ['xls', 'xlsx'], file_names)
    if len(excel_files) > 1:
        raise Exception, "More than one excel files found in the zipped folder."
    if len(excel_files) == 0:
        raise Exception, "No flashcard template excel file found in the zipped folder."

    file_contents = zfile.read(excel_files[0])
    path_to_excel = os.path.split(excel_files[0])[0]

    return [file_contents, zfile, file_names, path_to_excel]

def get_mappings_from_zip(deck, file_contents, file_names, zfile, path_to_excel, custom=False):
    """
    Checks if all the files in the excel file are in the zipped folder.
    Saves the files and returns the mappings between the file names and their paths
    """
    mappings = {'Image':{}, 'Audio':{}}

    if not utils.template_matches_file(deck.collection.card_template, file_contents):
        raise Exception, "The fields in the spreadsheet don't match those in the template."

    files = []
    files_not_found = []
    files_to_upload = utils.get_file_names(deck.collection.card_template, file_contents, custom=custom)
    for f in files_to_upload:
        file_map = {
            "absolute": os.path.join(path_to_excel, f),
            "relative": f
        }
        if file_map['absolute'] in file_names:
            files.append(file_map)
        else:
            files_not_found.append(file_map['relative'])

    if len(files_not_found):
        raise Exception, "File(s) not found in the zipped folder: %s" %str(files_not_found)[1:-1]

    temp_dir_path = tempfile.mkdtemp()
    for file in files:
        zfile.extract(file['absolute'], temp_dir_path)
        temp_file_path = os.path.join(temp_dir_path, file['absolute'])

        is_valid_image, errstr = valid_image_file_type(temp_file_path)
        if is_valid_image:
            store_file_name = handle_uploaded_media_file(temp_file_path, 'I')
            mappings['Image'][file['relative']] = store_file_name
        else:
            is_valid_audio, errstr = valid_audio_file_type(temp_file_path)
            if is_valid_audio:
                store_file_name = handle_uploaded_media_file(temp_file_path, 'A')
                mappings['Audio'][file['relative']] = store_file_name

    if len(files):
        shutil.rmtree(temp_dir_path)

    return [file_contents, mappings]

def handle_zipped_deck_file(deck, uploaded_file):
    """Handles uploaded zipped deck file (not customized)"""
    [file_contents, zfile, file_names, path_to_excel] = extract_from_zip(uploaded_file)
    [file_contents, mappings] = get_mappings_from_zip(deck, file_contents, file_names, zfile, path_to_excel)
    return [file_contents, mappings]

def handle_uploaded_deck_file(deck, uploaded_file):
    """Handles an uploaded deck file."""
    cached_file_contents = uploaded_file.read()
    mappings = None

    try:
        [file_contents, mappings] = handle_zipped_deck_file(deck, uploaded_file)
    except zipfile.BadZipfile:
        file_contents = cached_file_contents
        if not utils.template_matches_file(deck.collection.card_template, file_contents):
            raise Exception, "The fields in the spreadsheet don't match those in the template."

    try:
        parsed_cards = utils.parse_deck_template_file(deck.collection.card_template, file_contents, mappings)
    except:
        raise Exception, "Uploaded file type not supported."

    add_cards_to_deck(deck, parsed_cards)

def handle_custom_file(uploaded_file, course_name, user, is_teacher=False):
    """Handles an uploaded custom deck file."""
    cached_file_contents = uploaded_file.read()
    mappings = None
    try:
        [file_contents, zfile, file_names, path_to_excel] = extract_from_zip(uploaded_file)
        is_zip = True
    except zipfile.BadZipfile:
        file_contents = cached_file_contents
        is_zip = False
    if not utils.correct_custom_format(file_contents):
        raise Exception, "Incorrect format of the spreadsheet."
    card_template_fields = utils.get_card_template(file_contents)
    card_template = CardTemplate(title=course_name, owner=user)
    card_template.save()
    for template_field in card_template_fields:
        label = template_field['label']
        side = template_field['side']
        sort_order = template_field['sort_order']
        if side == 'Front':
            display = True
        else:
            display = False
        type = template_field['type'][0]
        field = Field(label=label, field_type=type, show_label=True, display=display, sort_order=sort_order)
        field.save()
        card_template_field = CardTemplates_Fields(card_template=card_template, field=field)
        card_template_field.save()
    collection = Collection(title=course_name, card_template=card_template, published=not is_teacher)
    collection.save()
    user_collection = Users_Collections(user=user, date_joined=date.today(), collection=collection, role=Users_Collections.ADMINISTRATOR)
    user_collection.save()
    deck = create_deck(collection_id=collection.id, deck_title='Untitled Deck')
    if is_zip:
        [file_contents, mappings] = get_mappings_from_zip(deck, file_contents, file_names, zfile, path_to_excel, custom=True)

    try:
        parsed_cards = utils.parse_deck_template_file(deck.collection.card_template, file_contents, mappings, custom=True)
    except:
        raise Exception, "Uploaded file type not supported."
    add_cards_to_deck(deck, parsed_cards)
    return deck


@transaction.atomic
def update_card_fields(card, field_items):
    field_ids = [f['field_id'] for f in field_items]
    field_map = dict((f['field_id'],f) for f in field_items)
    cfields = card.cards_fields_set.filter(field__id__in=field_ids)

    # update fields
    for cfield in cfields:
        field_id = cfield.field.id
        cfield.value = field_map[field_id]['value']
        cfield.save()
        field_map.pop(field_id)

    # create fields that did not exist
    if len(field_map) > 0:
        fields = Field.objects.all()
        for field_id, field_item in field_map.items():
            field_object = fields.get(pk=field_id)
            field_value = field_item['value']
            Cards_Fields.objects.create(card=card, field=field_object, value=field_value)
    return card

@transaction.atomic
def add_cards_to_deck(deck, card_list):
    """Adds a batch of cards with fields to a deck."""
    fields = Field.objects.all()
    card_sort_order = deck.collection.card_set.count()
    deck_sort_order = deck.cards.count()
    for card_item in card_list:
        card_sort_order = card_sort_order + 1
        deck_sort_order = deck_sort_order + 1
        card = Card.objects.create(collection=deck.collection, sort_order=card_sort_order)
        Decks_Cards.objects.create(deck=deck, card=card, sort_order=deck_sort_order)
        for field_item in card_item:
            field_object = fields.get(pk=field_item['field_id'])
            #if field_object.field_type == 'I':
            #    if field_item['value']:
            #        field_value = upload_img_from_path(field_item['value'], deck, deck.collection)
            #    else:
            #        field_value = field_item['value']
            #else:
            field_value = field_item['value']
            Cards_Fields.objects.create(card=card, field=field_object, value=field_value)
    return deck

@transaction.atomic
def create_deck_with_cards(collection_id, deck_title, card_list):
    """Creates and populates a new deck with cards."""
    collection = Collection.objects.get(id=collection_id)
    deck = create_deck(collection_id, deck_title)
    add_cards_to_deck(deck, card_list)
    return deck

@transaction.atomic
def create_card_in_deck(deck):
    fields = Field.objects.all()
    card_sort_order = deck.collection.card_set.count() + 1
    deck_sort_order = deck.cards.count() + 1
    card = Card.objects.create(collection=deck.collection, sort_order=card_sort_order)
    Decks_Cards.objects.create(deck=deck, card=card, sort_order=deck_sort_order)
    return card

def create_deck(collection_id, deck_title):
    collection = Collection.objects.get(id=collection_id)
    result = Deck.objects.filter(collection=collection).aggregate(Max('sort_order'))
    sort_order = result['sort_order__max']
    if sort_order is None:
        sort_order = 1
    else:
        sort_order = sort_order + 1
    deck = Deck.objects.create(title=deck_title, collection=collection, sort_order=sort_order)
    return deck

def has_role_with_request(request, roles, collection_id):
    """
    Checks if a particular user (based on the cached session) has
    a particular set of roles. Return True/False
    """
    role_bucket = get_or_update_role_bucket(request)
    return queries.has_role_in_bucket(role_bucket, roles, collection_id)

def get_or_update_role_bucket(request, collection_id = None, role = None):
    """ Get, create, and/or update the user's role_bucket.
        Returns the uptodate role_bucket dictionary.
    """
    role_bucket = request.session.get('role_bucket',{})

    if role_bucket and collection_id:
        if not role or not role_bucket.has_key(role):
            raise Exception("Invalid role provided. %s does not exist" % role)
        role_bucket[role].append(collection_id)
    else:
        role_bucket = Users_Collections.get_role_buckets(request.user)
        request.session['role_bucket'] = role_bucket

    return role_bucket

def add_user_to_collection(user=None, collection=None, role=None):
    if not (user and collection):
        return False

    exists = Users_Collections.objects.filter(user=user, collection=collection, role=role).exists()
    if exists:
        return True

    valid_roles = queries.getCollectionRoleList()
    if not role in valid_roles:
        raise Exception("invalid collection role")

    uc = Users_Collections.objects.create(user=user, collection=collection, role=role, date_joined=datetime.date.today())
    if uc:
        return True
    return False

def copy_collection(user, collection_id):
    """
    Deep copy of a collection.
    Returns the new collection object.
    """

    clone = Clone.objects.create(model='Collection', model_id=collection_id, cloned_by=user, status='Q')
    clone.status = 'P'
    clone.save()

    clone_ref = {'id': 0, 'fmt': str(clone.id) + ":%s", 'map': {}}
    clone_ref_map = clone_ref['map']

    def next_clone_ref_id():
        clone_ref['id'] += 1
        return clone_ref['fmt'] % clone_ref['id']

    ## Clone: COLLECTION
    collection = Collection.objects.get(pk=collection_id)
    old_collection_id = collection.id
    collection.id = None
    collection.title = "Copy of " + collection.title
    collection.save()
    new_collection = collection
    Cloned.objects.create(clone=clone, model='Collection', old_model_id=old_collection_id, new_model_id=new_collection.id)

    ## Clone: DECK
    decks = Deck.objects.filter(collection=old_collection_id)
    deck_map = {}
    deck_copies = []
    deck_ref_ids = []
    for deck in decks:
        old_deck_id = deck.id

        deck.id = None
        deck.collection = new_collection
        deck.clone_ref_id = next_clone_ref_id()
        deck_copies.append(deck)

        deck_ref_ids.append(deck.clone_ref_id)
        clone_ref_map[deck.clone_ref_id] = {
            "model": "Deck",
            "old_model_id": old_deck_id
        }

    # bulk create the deck copies and lookup the new IDs
    Deck.objects.bulk_create(deck_copies)
    for deck in Deck.objects.filter(clone_ref_id__in=deck_ref_ids):
        old_deck_id = clone_ref_map[deck.clone_ref_id]['old_model_id']
        clone_ref_map[deck.clone_ref_id]['new_model_id'] = deck.id
        deck_map[old_deck_id] = deck

    ## Clone: DECKS_CARDS and CARD
    card_map = {}
    if deck_map.keys():
        # find all the cards that need to be copied
        decks_cards = Decks_Cards.objects.filter(deck__in=deck_map.keys()).select_related('deck','card')
        card_copies = []
        card_ref_ids = []
        for decks_cards_item in decks_cards:
            card = decks_cards_item.card
            old_card_id = card.id

            card.id = None
            card.collection = new_collection
            card.clone_ref_id = next_clone_ref_id()
            card_copies.append(card)

            card_ref_ids.append(card.clone_ref_id)
            clone_ref_map[card.clone_ref_id] = {
                "model": "Card",
                "old_model_id": old_card_id,
            }

        # bulk create the card copies and lookup the new IDs
        Card.objects.bulk_create(card_copies)
        for card in Card.objects.filter(clone_ref_id__in=card_ref_ids):
            old_card_id = clone_ref_map[card.clone_ref_id]['old_model_id']
            clone_ref_map[card.clone_ref_id]['new_model_id'] = card.id
            card_map[old_card_id] = card

        # find all the decks_cards that need to be copied
        decks_cards = Decks_Cards.objects.filter(deck__in=deck_map.keys()).select_related('deck','card')
        decks_cards_copies = []
        decks_cards_ref_ids = []
        for decks_cards_item in decks_cards:
            card = decks_cards_item.card
            old_card_id = card.id
            old_decks_cards_id = decks_cards_item.id
            old_deck_id = decks_cards_item.deck.id

            decks_cards_item.id = None
            decks_cards_item.deck = deck_map[old_deck_id]
            decks_cards_item.card = card_map[old_card_id]
            decks_cards_item.clone_ref_id = next_clone_ref_id()
            decks_cards_copies.append(decks_cards_item)

            decks_cards_ref_ids.append(decks_cards_item.clone_ref_id)
            clone_ref_map[decks_cards_item.clone_ref_id] = {
                "model": "Card",
                "old_model_id": old_card_id,
            }

        # bulk create the card copies and lookup the new IDs
        Decks_Cards.objects.bulk_create(decks_cards_copies)
        for decks_cards_item in Decks_Cards.objects.filter(clone_ref_id__in=decks_cards_ref_ids):
            old_decks_cards_id = clone_ref_map[decks_cards_item.clone_ref_id]['old_model_id']
            clone_ref_map[decks_cards_item.clone_ref_id]['new_model_id'] = decks_cards_item.id

    ## Clone: CARDS_FIELDS
    cards_fields_copies = []
    cards_fields_ref_ids = []
    if card_map.keys():
        cards_fields = Cards_Fields.objects.filter(card__in=card_map.keys()).select_related('card')
        for cards_fields_item in cards_fields:
            old_cards_fields_id = cards_fields_item.id
            old_card_id = cards_fields_item.card.id
            cards_fields_item.card = card_map[old_card_id]
            cards_fields_item.id = None
            cards_fields_item.clone_ref_id = next_clone_ref_id()
            cards_fields_copies.append(cards_fields_item)

            cards_fields_ref_ids.append(cards_fields_item.clone_ref_id)
            clone_ref_map[cards_fields_item.clone_ref_id] = {
                "model": "Cards_Fields",
                "old_model_id": old_card_id,
            }

    # bulk create the cards_fields and lookup the new IDs
    Cards_Fields.objects.bulk_create(cards_fields_copies)
    for cards_fields_item in Cards_Fields.objects.filter(clone_ref_id__in=cards_fields_ref_ids):
        old_cards_fields_id = clone_ref_map[cards_fields_item.clone_ref_id]['old_model_id']
        clone_ref_map[cards_fields_item.clone_ref_id]['new_model_id'] = cards_fields_item.id

    ## Save the audited list of cloned objects
    cloned_objects = []
    sorted_clone_ref_ids = sorted(clone_ref_map.keys(), key=lambda x: int(x.split(':')[1]))
    for clone_ref_id in sorted_clone_ref_ids:
        clone_ref = clone_ref_map[clone_ref_id]
        cloned_obj = Cloned(
            clone=clone,
            model=clone_ref['model'],
            old_model_id=clone_ref['old_model_id'],
            new_model_id=clone_ref['new_model_id'])
        cloned_objects.append(cloned_obj)

    # bulk create the cloned objects
    Cloned.objects.bulk_create(cloned_objects)

    # set status to done
    clone.status = 'D'
    clone.save()

    return new_collection
