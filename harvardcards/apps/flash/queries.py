""" 
This module contains common queries that return a result and DO NOT change the
observable state of the system (are free of side effects).
"""

from harvardcards.apps.flash.models import Collection, Deck, Decks_Cards

def getDecksByCollection():
    """gets the decks associated with a collection"""
    decks = Deck.objects.all().prefetch_related('collection', 'cards')
    decks_by_collection = {}
    for deck in decks:
        if deck.collection.id not in decks_by_collection:
            decks_by_collection[deck.collection.id] = []
        decks_by_collection[deck.collection.id].append(deck)
    return decks_by_collection

def getDeckCollectionId(deck_id):
    """gets the collection id associated with the deck"""
    return Deck.objects.get(id=deck_id).collection.id
        
def getCollection(collection_id):
    """get a collection object from its id"""
    collection = Collection.objects.filter(id=collection_id)
    if not collection:
        return False
    else:
        return collection[0]

def getFieldList(collection_id):
    """get the fields associated with the collection"""
    collection = Collection.objects.get(id=collection_id)
    fields = collection.card_template.fields.all().order_by('sort_order')
    return [{
        'id': field.id,
        'label': field.label,
        'show_label': field.show_label,
        'field_type': field.field_type,
        'sort_order': field.sort_order,
        'display': field.display,
    } for field in fields]

def getDeckCardsList(deck_id):
    deck = Deck.objects.get(id=deck_id)
    deck_cards = Decks_Cards.objects.filter(deck=deck).order_by('sort_order').prefetch_related('card__cards_fields_set__field')

    card_list = []
    for dcard in deck_cards:
        card_fields = []
        for cfield in dcard.card.cards_fields_set.all():
            card_fields.append({
                'field_id': cfield.field.id,
                'type': cfield.field.field_type,
                'label': cfield.field.label,
                'show_label': cfield.field.show_label,
                'display': cfield.field.display,
                'value': cfield.value,
            })
        card_list.append({
            "card_id": dcard.card.id,
            "fields": card_fields,
        })

    return card_list

def isCardInDeck(card_id, deck_id):
    if Decks_Cards.objects.filter(card=card_id, deck=deck_id):
        return True
    return False
