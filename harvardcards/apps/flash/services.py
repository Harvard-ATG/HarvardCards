"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""
import urllib2
import os
import shutil
import datetime
import zipfile
import hashlib
import tempfile
import mimetypes
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

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields, Field, Users_Collections, CardTemplate, CardTemplates_Fields, Clone, Cloned, MediaStore
from harvardcards.apps.flash import utils
from harvardcards.apps.flash import queries
from harvardcards.settings.common import MEDIA_ROOT, APPS_ROOT


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
    try:
        img = Image.open(file_path)
        img_type = (img.format).lower()
        if img_type not in ['rgb', 'gif', 'png', 'bmp', 'gif', 'jpeg']:
            return False
    except:
        return False
    return True

def valid_audio_file_type(file_path):
    """Returns true if the given file is a valid audio type."""
    try:
        audio = MP3(file_path)
    except:
        return False
    return True

def handle_uploaded_media_file(file, type=None):
    """Handles an uploaded file and returns the path to the file object."""
    store_service = MediaStoreService(file=file)
    store_service.save(type)
    return store_service.storeFileName()

def fetch_image_from_url(file_url):
    """Returns an UploadedFile object after retrieving the file at the given URL."""
    inStream = urllib2.urlopen(file_url)

    parser = ImageFile.Parser()
    file_size = 0
    read_size = 1024
    while True:
        s = inStream.read(read_size)
        file_size += len(s)
        if not s:
            break
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
            if f['type'] != 'T':
                field_set.add(f['value'])

    # add each media object ot the zip file 
    for file_name in field_set:
        file_path = MediaStoreService.getAbsPathToOriginal(file_name)
        if os.path.exists(file_path):
            zfile.write(file_path, arcname=file_name)

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

        if valid_image_file_type(temp_file_path):
            store_file_name = handle_uploaded_media_file(temp_file_path, 'I')
            mappings['Image'][file['relative']] = store_file_name

        elif valid_audio_file_type(temp_file_path):
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

def handle_custom_file(uploaded_file, course_name, user, is_teacher):
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

def copy_collection(user, collection_id):
    """
    Deep copy of a collection.
    Returns the new collection object.
    """

    clone = Clone.objects.create(model='Collection', model_id=collection_id, cloned_by=user, status='Q')
    clone.status = 'P'
    clone.save()

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
    for deck in decks:
        old_deck_id = deck.id
        deck.id = None
        deck.collection = new_collection
        deck.save()
        new_deck = deck
        deck_map[old_deck_id] = new_deck
        Cloned.objects.create(clone=clone, model='Deck', old_model_id=old_deck_id, new_model_id=new_deck.id)

    ## Clone: DECKS_CARDS and CARD
    card_map = {}
    if deck_map.keys():
        decks_cards = Decks_Cards.objects.filter(deck__in=deck_map.keys()).select_related('deck','card')
        for decks_cards_item in decks_cards:
            card = decks_cards_item.card
            old_card_id = card.id
            card.id = None
            card.collection = new_collection
            card.save()
            new_card = card
            card_map[old_card_id] = new_card
            Cloned.objects.create(clone=clone, model='Card', old_model_id=old_card_id, new_model_id=new_card.id)

            old_decks_cards_id = decks_cards_item.id
            old_deck_id = decks_cards_item.deck.id
            decks_cards_item.deck = deck_map[old_deck_id]
            decks_cards_item.card = new_card
            decks_cards_item.id = None
            decks_cards_item.save()
            new_decks_cards_item = decks_cards_item
            Cloned.objects.create(clone=clone, model='Decks_Cards', old_model_id=old_decks_cards_id, new_model_id=new_decks_cards_item.id)

    ## Clone: CARDS_FIELDS
    if card_map.keys():
        cards_fields = Cards_Fields.objects.filter(card__in=card_map.keys()).select_related('card')
        for cards_fields_item in cards_fields:
            old_cards_fields_id = cards_fields_item.id
            old_card_id = cards_fields_item.card.id
            cards_fields_item.card = card_map[old_card_id]
            cards_fields_item.id = None
            cards_fields_item.save()
            new_cards_fields = cards_fields_item
            Cloned.objects.create(clone=clone, model='Cards_Fields', old_model_id=old_cards_fields_id, new_model_id=new_cards_fields.id)

    clone.status = 'D'
    clone.save()

    return new_collection


class MediaStoreService:
    """Class to manage reading and writings files to the local media store."""

    def __init__(self, *args, **kwargs):
        file = kwargs.get('file', None)

        if isinstance(file, basestring):
            if os.path.exists(file):
                file_object = open(file, 'r')
                file_name = os.path.split(file)[1]
                file_type = mimetypes.guess_type(file_name)[0]
                file_size = os.path.getsize(file)
                file = UploadedFile(
                    file=file_object, 
                    name=file_name, 
                    content_type=file_type, 
                    size=file_size, 
                    charset=None
                )

        if not isinstance(file, UploadedFile):
            raise Exception("Error handling file: MediaStoreService expects UploadedFile")

        self._file_md5hash = None
        self.file = file
        self._createBaseDirs()

    def save(self, type=None):
        """Saves the media store."""

        if self.fileRecordExists():
            store = self.lookupFileRecord()
        else:
            self.writeFile()
            self.process(type)
            self.link(type)
            store = self.createFileRecord()
            store.save()

        return store

    def process(self, type=None):
        if type == 'I':
            self._processResizeImage()

    def link(self, type=None):
        file_name = self.storeFileName()

        # link to the original media file
        original_source_path = os.path.join('..', '..', self.storeFilePath('original'))
        original_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'original', file_name))
        if not os.path.lexists(original_link_path):
            os.symlink(original_source_path, original_link_path)

        if type == 'I':
            # link to the large thumbnail file
            large_source_path = os.path.join('..', '..', self.storeFilePath('thumb-large'))
            large_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-large', file_name))
            if not os.path.lexists(large_link_path):
                os.symlink(large_source_path, large_link_path)

            # link to the small thumbnail file
            small_source_path = os.path.join('..', '..', self.storeFilePath('thumb-small'))
            small_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-small', file_name))
            if not os.path.lexists(small_link_path):
                os.symlink(small_source_path, small_link_path)


    def writeFile(self):
        file = self.file
        file_name = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        with open(file_name, 'wb+') as dest:
            if file.multiple_chunks:
                for c in file.chunks():
                    dest.write(c)
            else:
                dest.write(file.read())

    def fileHash(self):
        if self._file_md5hash:
            return self._file_md5hash

        m = hashlib.md5()
        if self.file.multiple_chunks:
            for chunk in self.file.chunks():
                m.update(chunk)
        else:
            m.update(self.file.read())

        self._file_md5hash = m.hexdigest()

        return self._file_md5hash

    def createFileRecord(self):
        return MediaStore(
            file_name=self.storeFileName(),
            file_size=self.file.size,
            file_type=self.file.content_type,
            file_md5hash=self.fileHash()
        )

    def fileRecordExists(self):
        return MediaStore.objects.filter(file_md5hash=self.fileHash()).exists()

    def lookupFileRecord(self):
        return MediaStore.objects.filter(file_md5hash=self.fileHash())[0]

    def storeDir(self):
        return 'store'

    def storeFileDir(self):
        return os.path.join(self.storeDir(), self.fileHash())

    def storeFileName(self):
        file_extension = os.path.splitext(self.file.name)[1]
        return self.fileHash() + file_extension.lower()

    def storeFilePath(self, path):
        return os.path.join(self.storeFileDir(), path, self.storeFileName())

    def _createBaseDirs(self):
        file_paths = [
            MEDIA_ROOT,
            os.path.join(MEDIA_ROOT, self.storeDir()),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'original'),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-large'),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-small'),
            os.path.join(MEDIA_ROOT, self.storeFileDir()),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'original'),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'thumb-large'),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'thumb-small'),
        ]
        for p in file_paths:
            if not os.path.exists(p):
                os.mkdir(p)

    def _processResizeImage(self):
        """
        Resizes an uploaded image. Saves both the original, thumbnail, and resized versions.
        """

        original_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        thumb_large_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-large')))
        thumb_small_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-small')))

        img = Image.open(original_path)

        # create large thumbnail
        width, height = img.size
        new_height = 600;
        max_width = 1000;
        if height > new_height:
            new_width = width*new_height/float(height);
            img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            img_anti.save(thumb_large_path)
        else:
            if width > max_width:
                new_height = height*max_width/float(width)
                img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
                img_anti.save(thumb_large_path)
            else:
                img.save(thumb_large_path)

        # create small thumbnail
        t_height = 150
        t_width = width*t_height/float(height)
        img_thumb = img.resize((int(t_width), int(t_height)), Image.ANTIALIAS)
        img_thumb.save(thumb_small_path)

    @classmethod
    def getAbsPathToStore(cls):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store'))

    @classmethod
    def getAbsPathToOriginal(cls, file_name):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store', 'original', file_name))



