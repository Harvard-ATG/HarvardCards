""" 
This module contains common queries that return a result and DO NOT change the
observable state of the system (are free of side effects).
"""

from harvardcards.apps.flash.models import Collection, Deck

def getDecksByCollection():
    """gets the decks associated with a collection"""
    decks = Deck.objects.all().prefetch_related('collection', 'cards')
    decks_by_collection = {}
    for deck in decks:
        if deck.collection.id not in decks_by_collection:
            decks_by_collection[deck.collection.id] = []
        decks_by_collection[deck.collection.id].append(deck)
    return decks_by_collection
        
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
    fields = collection.field_set.all().order_by('sort_order')
    field_list = []
    for field in fields:
        f = {}
        f['label'] = field.label
        f['id'] = field.id
        f['field_type'] = field.field_type
        f['sort_order'] = field.sort_order
        f['display'] = field.display
        field_list.append(f)
    return field_list
