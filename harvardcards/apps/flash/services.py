"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""
from django.db import transaction

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields, Field
from harvardcards.apps.flash import utils 

def delete_collection(collection_id):
    """Deletes a collection and returns true on success, false otherwise."""
    Collection.objects.get(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    return False

def delete_deck(deck_id):
    """Deletes a deck and returns true on success, false otherwise."""
    Deck.objects.get(id=deck_id).delete()
    if not Deck.objects.filter(id=deck_id):
        return True
    return False

def delete_card(card_id):
    """Deletes a card and returns true on success, false otherwise."""
    Card.objects.get(id=card_id).delete()
    if not Deck.objects.filter(id=card_id):
        return True
    return False
    
def handle_uploaded_deck_file(collection_id, deck_title, uploaded_file):
    """Handles an uploaded deck."""
    collection = Collection.objects.get(id=collection_id)
    file_contents = uploaded_file.read()
    parsed_cards = utils.parse_deck_template_file(collection.card_template, file_contents)
    deck = create_deck_with_cards(collection_id, deck_title, parsed_cards)

    return deck

@transaction.commit_on_success
def add_cards_to_deck(deck, card_list):
    """Adds a list of cards with fields to a deck."""
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
