""" 
This module contains common queries that return a result and DO NOT change the
observable state of the system (are free of side effects).
"""

from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Decks_Cards

import logging
log = logging.getLogger(__name__)

def is_superuser_or_staff(user):
    """ Checks if the user is superuser or staff. Returns True or False """
    return user.is_staff or user.is_superuser

def has_role_in_bucket(role_bucket, roles, collection_id):
    """
    Checks if the collection id has any roles in the bucket.
    Returns true if the collection id maps to any of the given roles,
    False otherwise.
    """
    role_map = Users_Collections.role_map
    for role in roles:
        if collection_id in role_bucket[role_map[role]]:
            return True
    return False

def getCollectionRoleList():
    """gets a list of roles that may grant access to a collection """
    role_list = [
        Users_Collections.ADMINISTRATOR, 
        Users_Collections.INSTRUCTOR, 
        Users_Collections.TEACHING_ASSISTANT, 
        Users_Collections.CONTENT_DEVELOPER, 
        Users_Collections.LEARNER]
    return role_list

def getCollectionList(role_bucket):
    """gets the list of collections that the user has permission to access"""
    log.debug("getCollectionList()")
    log.debug("role_bucket = %s" % role_bucket)

    all_collections = Collection.objects.all()
    decks_by_collection = getDecksByCollection()
    collection_roles = getCollectionRoleList()

    collection_list = []
    for collection in all_collections:
        has_access = True
        has_access = has_access and not collection.private
        has_access = has_access or has_role_in_bucket(role_bucket, collection_roles, collection.id)
        log.debug("collection id: [%s] has access: [%s]" % (collection.id, has_access))
        if has_access:
            collection_decks = []
            log.debug("decks for collection id [%s]: %s" % (collection.id, decks_by_collection.get(collection.id, None)))
            if decks_by_collection.get(collection.id, False):
                for deck in decks_by_collection[collection.id]:
                    collection_decks.append({
                        'id': deck.id,
                        'title': deck.title,
                        'num_cards': deck.cards.count()
                    })
                collection_list.append({
                    'id': collection.id,
                    'title':collection.title,
                    'decks': collection_decks
                })
            else:
                collection_list.append({
                    'id': collection.id,
                    'title':collection.title,
                    'decks': []
                })

    return collection_list

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
