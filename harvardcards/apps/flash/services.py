"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""
import urllib2
import os
import shutil
import datetime
from  PIL import Image

from django.db import transaction
from django.db.models import Avg, Max, Min
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, PermissionDenied

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields, Field, Users_Collections, CardTemplate, CardTemplates_Fields
from harvardcards.apps.flash import utils
from harvardcards.apps.flash import queries
from harvardcards.settings.common import MEDIA_ROOT, APPS_ROOT
import zipfile
from StringIO import StringIO
from mutagen.mp3 import MP3
from sets import Set
from datetime import date


def delete_collection(collection_id):
    """Deletes a collection and returns true on success, false otherwise."""
    Collection.objects.get(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    return False

def delete_deck(deck_id):
    """Deletes a deck and returns true on success, false otherwise."""
    deck = Deck.objects.get(id=deck_id)
    delete_deck_files(deck_id)
    deck.delete()
    if not Deck.objects.filter(id=deck_id):
        return True
    return False

def delete_deck_files(deck_id):
    """
    Deletes all the files (images, audio) associated with the deck. 
    Raises an exception if there is a problem deleting the images.
    """
    deck = Deck.objects.get(id=deck_id)
    folder_name = utils.get_media_folder_name(deck)
    folder_paths = [
        os.path.abspath(os.path.join(MEDIA_ROOT, folder_name)),
        os.path.abspath(os.path.join(MEDIA_ROOT,'thumbnails', folder_name)),
        os.path.abspath(os.path.join(MEDIA_ROOT,'originals', folder_name)),
    ]
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

def delete_card(card_id):
    """Deletes a card and returns true on success, false otherwise."""
    Card.objects.get(id=card_id).delete()
    if not Card.objects.filter(id=card_id):
        return True
    return False

def resize_uploaded_img(path, file_name, dir_name):
    """
    Resizes an uploaded image. Saves both the original, thumbnail, and
    resized versions.
    """
    full_path = os.path.join(path, file_name)

    img = Image.open(full_path)

    # original
    path1 = os.path.abspath(os.path.join(MEDIA_ROOT, 'originals', dir_name))
    if not os.path.exists(path1):
        os.makedirs(path1)
    img.save(os.path.join(path1, file_name))

    # resized
    width, height = img.size
    new_height = 600;
    max_width = 1000;
    if height > new_height:
        new_width = width*new_height/float(height);
        img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        img_anti.save(full_path)
    else:
        if width > max_width:
            new_height = height*max_width/float(width)
            img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            img_anti.save(full_path)

    # thumbnail
    path1 = os.path.abspath(os.path.join(MEDIA_ROOT, 'thumbnails', dir_name))
    if not os.path.exists(path1):
        os.makedirs(path1)

    t_height = 150
    t_width = width*t_height/float(height)
    img_thumb = img.resize((int(t_width), int(t_height)), Image.ANTIALIAS)
    img_thumb.save(os.path.join(path1, file_name))

def valid_uploaded_file(uploaded_file, file_type):
    if file_type == 'I':
        try:
            img = Image.open(uploaded_file)
            img_type = (img.format).lower()
            if img_type not in ['rgb', 'gif', 'png', 'bmp', 'gif', 'jpeg']:
                return False
        except:
            return False
        return True

    if file_type == 'A':
        try:
            audio = MP3(uploaded_file)
        except:
            return False
        return True

def handle_media_folders(deck, file_name):
    """
    Returns media folder info for a given file in a deck.
    If the given file name is a duplicate of a file already associated 
    with the deck, it will automatically be given a new name.
    """
    [dir_name, path, path_images] = utils.get_media_path(deck)

    # allow files with same names to be uploaded to the same deck
    file_name = os.path.split(file_name)[1]
    original_filename = file_name
    full_path = os.path.join(path, file_name)

    counter = 1
    while os.path.exists(full_path):
        file_name = str(counter)+ '_' + original_filename
        full_path = os.path.join(path, file_name)
        counter = counter + 1

    return [full_path, path, dir_name, file_name]

def handle_uploaded_img_file(file, deck, collection):
    """Handles an uploaded image file and returns the path to the saved image."""

    file_name = file.name
    [full_path, path, dir_name, file_name] = handle_media_folders(deck, file_name)
    dest = open(full_path, 'wb+')
    if file.multiple_chunks:
        for c in file.chunks():
            dest.write(c)
    else:
        dest.write(file.read())
    dest.close()
    resize_uploaded_img(path, file_name, dir_name)

    return os.path.join(dir_name, file_name)

def upload_img_from_path(path_original, deck, collection):
    head, file_name = os.path.split(path_original)
    [full_path, path, dir_name, file_name] = handle_media_folders(deck.id, file_name)
    try:
        webpage = urllib2.urlopen(path_original)
        img = open(full_path,"wb")
        img.write(webpage.read())
        img.close()
    except:
        img = Image.open(path_original)
        img.save(full_path)
    resize_uploaded_img(path, file_name, dir_name)
    return os.path.join(dir_name, file_name)

def create_zip_deck_file(deck):
    [folder_name, path, path_images] = utils.get_media_path(deck.id)
    s = StringIO()

    zfile = zipfile.ZipFile(s, "w")

    file_output = utils.create_deck_file(deck.id)
    deck_file = os.path.join(path, 'deck_file.xls')
    file_output.save(deck_file)

    images = []
    if os.path.exists(path_images):
        images = os.listdir(path_images)

    for file in os.listdir(path):
        if file.endswith('.db') or file.startswith('.'):
            continue
        if file in images:
            file_path = path_images
        else:
            file_path = path
        zfile.write(os.path.join(file_path, file), arcname=file)
    zfile.close()
    os.remove(deck_file)
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

    for file in files:
        [full_path, path, dir_name, file_name] = handle_media_folders(deck.id, file['relative'])
        zfile.extract(file['absolute'], os.path.join(path, 'temp_dir'))
        file_path = os.path.join(path, 'temp_dir', file['absolute'])

        if valid_uploaded_file(file_path, 'I'):
            os.rename(file_path, os.path.join(path, 'temp_dir', file_name))
            shutil.move(os.path.join(path, 'temp_dir', file_name), os.path.join(path, file_name))
            resize_uploaded_img(path, file_name, dir_name)
            mappings['Image'][file['relative']] = os.path.join(dir_name, file_name)

        elif valid_uploaded_file(file_path, 'A'):
            os.rename(file_path, os.path.join(path, 'temp_dir', file_name))
            shutil.move(os.path.join(path, 'temp_dir', file_name), os.path.join(path, file_name))
            mappings['Audio'][file['relative']] = os.path.join(dir_name, file_name)

    if len(files):
        shutil.rmtree(os.path.join(path, 'temp_dir'))
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

def handle_custom_file(uploaded_file, course_name, user):
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

    collection = Collection(title=course_name, card_template=card_template)
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


@transaction.commit_on_success
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

@transaction.commit_on_success
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

@transaction.commit_on_success
def create_deck_with_cards(collection_id, deck_title, card_list):
    """Creates and populates a new deck with cards."""
    collection = Collection.objects.get(id=collection_id)
    deck = create_deck(collection_id, deck_title)
    add_cards_to_deck(deck, card_list)
    return deck

@transaction.commit_on_success
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

