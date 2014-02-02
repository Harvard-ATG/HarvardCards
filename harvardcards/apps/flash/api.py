from django.utils import simplejson as json
from django.core import serializers

from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field

def getDecksByCollection():
    decks = Deck.objects.all().prefetch_related('collection', 'cards')
    decks_by_collection = {}
    for deck in decks:
        if deck.collection.id not in decks_by_collection:
            decks_by_collection[deck.collection.id] = []
        decks_by_collection[deck.collection.id].append(deck)
    return decks_by_collection
        
def deleteCollection(collection_id):
    Collection.objects.filter(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return json.dumps(True)
    else:
        return json.dumps(False)
    

def getCollection(collection_id):
    collection = Collection.objects.filter(id=collection_id)
    if not collection:
        return False
    else:
        return serializers.serialize('json', collection)
