"""
This module contains services and commands that may change the state of the system
(i.e. called for their side effects).
"""

from harvardcards.apps.flash.models import Collection, Deck, Card, Decks_Cards, Cards_Fields
from harvardcards.apps.flash import utils 

def delete_collection(collection_id):
    """Deletes a collection and returns true on success, false otherwise."""
    Collection.objects.filter(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    return False
    
def handle_uploaded_deck(collection_id, deck_title, uploaded_file):
    """Handles an uploaded deck by parsing the rows as cards and the columns as fields."""

    collection = Collection.objects.get(id=collection_id)
    collection_n = collection.card_set.count()
    deck_n = 0

    file_contents = uploaded_file.read()
    parsed_cards = utils.parse_deck_template_file(collection.card_template, file_contents)

    deck = Deck(title=deck_title, collection=collection)
    deck.save()

    for parsed_card in parsed_cards:
        collection_n = collection_n + 1
        deck_n = deck_n + 1
        card = Card(collection=collection, sort_order=collection_n)
        card.save()
        for field in parsed_card:
            card_fields = Cards_Fields(card=card, field=field['field'], value=field['value'])
            card_fields.save()
        deck_cards = Decks_Cards(deck=deck, card=card, sort_order=deck_n)
        deck_cards.save()

    return {"success":True, "deck_id":deck.id}
