"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""
from django.db import transaction

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields, Field
from harvardcards.apps.flash import utils, queries
import os
import shutil
from harvardcards.settings.common import MEDIA_ROOT, APPS_ROOT
from  PIL import Image
import urllib2
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def delete_collection(collection_id):
    """Deletes a collection and returns true on success, false otherwise."""
    Collection.objects.get(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    return False

def delete_deck(deck_id):
    """Deletes a deck and returns true on success, false otherwise."""
    deck = Deck.objects.get(id=deck_id)
    delete_deck_images(deck_id)
    deck.delete()
    if not Deck.objects.filter(id=deck_id):
        return True
    return False

def delete_deck_images(deck_id):
    """
    Deletes all the images associated with a deck. 
    Raises an exception if there is a problem deleting the images.
    """
    deck = Deck.objects.get(id=deck_id)
    folder_name = str(deck.collection.id) + '_' + str(deck.id)
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
        except:
            return False
        return True

def handle_media_folders(collection, deck, file_name):
    # create the MEDIA_ROOT folder if it doesn't exist
    if not os.path.exists(MEDIA_ROOT):
        os.mkdir(MEDIA_ROOT)

    # folder where media files will be uploaded for the given deck
    dir_name = str(collection) +'_' + str(deck)
    path = os.path.abspath(os.path.join(MEDIA_ROOT, dir_name))
    if not os.path.exists(path):
        os.mkdir(path)
    # allow files with same names to be uploaded to the same deck
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
    [full_path, path, dir_name, file_name] = handle_media_folders(collection, deck, file_name)
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
    [full_path, path, dir_name, file_name] = handle_media_folders(collection.id, deck.id, file_name)
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


def handle_uploaded_deck_file(deck, uploaded_file):
    """Handles an uploaded deck file."""
    file_contents = uploaded_file.read()
    parsed_cards = utils.parse_deck_template_file(deck.collection.card_template, file_contents)
    add_cards_to_deck(deck, parsed_cards)
 
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
            if field_object.field_type == 'I':
                field_value = upload_img_from_path(field_item['value'], deck, deck.collection)
            else:
                field_value = field_item['value']
            Cards_Fields.objects.create(card=card, field=field_object, value=field_value)
    return deck

@transaction.commit_on_success
def create_deck_with_cards(collection_id, deck_title, card_list):
    """Creates and populates a new deck with cards."""
    collection = Collection.objects.get(id=collection_id)
    deck = Deck.objects.create(title=deck_title, collection=collection)
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
