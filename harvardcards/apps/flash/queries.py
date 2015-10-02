""" 
This module contains common queries that return a result and DO NOT change the
observable state of the system (are free of side effects).
"""

from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Decks_Cards, Course, Course_Map

import logging
log = logging.getLogger(__name__)

def get_course_collection_ids():
    return Course_Map.objects.all().values_list('collection_id', flat=True)

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

def groupCollectionsByList(collection_list):
    """groups collections into 'course' vs 'private' collections"""

    group_of = {
        "num_collections": 0,
        "course": {
            "label": "Course Collections",
            "collections": [],
            "num_collections": 0,
            "num_published": 0,
            "num_unpublished": 0,
        },
        "private": {
            "label": "Private Collections",
            "collections": [],
            "num_collections": 0,
            "num_published": 0,
            "num_unpublished": 0,
        },
        "groups": []
    }
    
    course_collection_map = {}
    course_collections = Course_Map.objects.all()
    for course_collection in course_collections:
        collection_id = course_collection.collection.id
        if collection_id not in course_collection_map:
            course_collection_map[collection_id] = course_collection

    for collection in collection_list:
        if collection['id'] in course_collection_map:
            group_key = 'course'
        else:
            group_key = 'private'

        if collection['published']:
            publish_key = 'num_published'
        else:
            publish_key = 'num_unpublished'

        group_of[group_key]['collections'].append(collection)
        group_of[group_key]['num_collections'] += 1
        group_of[group_key][publish_key] += 1
        group_of['num_collections'] += 1
        
    group_of['groups'] = [group_of['course'], group_of['private']]
    
    return group_of

def getCollectionList(role_bucket, **kwargs):
    """gets the list of collections that the user has permission to access"""
    log.debug("getCollectionList()")

    def add_all_card_deck(collection):
        decks = collection['decks']
        num_cards = sum(map(lambda d: d['num_cards'], decks))
        if num_cards:
            collection['decks'] = [{'title': 'All Cards', 'id':-collection['id'], 'num_cards': num_cards}] + collection['decks']
        return collection

    can_filter = kwargs.get('can_filter', True)
    collection_ids = kwargs.get('collection_ids', [])
    log.debug("role_bucket = %s collection_ids = %s can_filter= %s " % (role_bucket, collection_ids, can_filter))
    
    collections = Collection.objects.all()

    course_ids = get_course_collection_ids()
    if can_filter:
        other_course_collections = [c for c in course_ids if c not in collection_ids]
        collections = collections.exclude(id__in=other_course_collections)

    decks_by_collection = getDecksByCollection(**kwargs)

    collection_roles = getCollectionRoleList()

    collection_list = []
    for collection in collections:
        has_access = has_role_in_bucket(role_bucket, collection_roles, collection.id)
        log.debug("collection id: [%s] has access: [%s]" % (collection.id, has_access))

        if collection.id in role_bucket[Users_Collections.role_map[Users_Collections.LEARNER]]:
            has_access = has_access and collection.published
            log.debug("checking access based on whether collection is published: %s" % has_access)
        
        if has_access:
            collection_decks = []
            log.debug("decks for collection id [%s]: %s" % (collection.id, decks_by_collection.get(collection.id, None)))
            if decks_by_collection.get(collection.id, False):
                for deck in decks_by_collection[collection.id]:
                    collection_decks.append({
                        'id': deck.id,
                        'title': deck.title,
                        'num_cards': deck.cards__count
                    })
                collection_item = {
                    'id': collection.id,
                    'title':collection.title,
                    'published': collection.published,
                    'decks': collection_decks
                }
            else:
                collection_item = {
                    'id': collection.id,
                    'title':collection.title,
                    'published': collection.published,
                    'decks': []
                }
            collection_item = add_all_card_deck(collection_item)
            collection_list.append(collection_item)

    return collection_list

def getDecksByCollection(*args, **kwargs):
    """gets the decks associated with a collection"""
    from django.db.models import Count
    can_filter = kwargs.get('can_filter', True)
    collection_ids = kwargs.get('collection_ids', [])

    decks = Deck.objects.all().select_related('collection').annotate(Count('cards'))
    if can_filter:
        decks = decks.filter(collection__id__in=collection_ids)
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

def getDeckIds(collection_id):
    """Returns the deck ids associated with a collection"""
    decks = Deck.objects.filter(collection=collection_id)
    deck_ids = map(lambda d: d.id, decks) if len(decks) else []
    return deck_ids

def getDeckIdCard(card_id, collection_id):
    deck_ids = getDeckIds(collection_id)
    for deck_id in deck_ids:
        if isCardInDeck(card_id, deck_id):
            return deck_id
    else:
        return None

def isCardInDeck(card_id, deck_id):
    if Decks_Cards.objects.filter(card=card_id, deck=deck_id):
        return True
    return False

def can_copy_collection(user, collection_id):
    if is_superuser_or_staff(user):
        return True

    is_member = Users_Collections.objects.filter(user=user, collection=collection_id).exists()
    if is_member:
        return True
    return False

def getCourseNameCollectionMap():
    '''Returns a dictionary that maps collection IDs to canvas course short names.'''
    id_to_course_name = dict([
        (c.course_id, c.course_name_short)
        for c in Course.objects.all()
    ])
    collection_to_course_name = dict([
        (cm.collection_id, id_to_course_name.get(cm.course_id, ''))
        for cm in Course_Map.objects.all()
    ])
    return collection_to_course_name

def getCopyCollectionList(user):
    '''Returns a list of collections that the given user may copy.'''
    collections = []
    if is_superuser_or_staff(user):
        collections = Collection.objects.all().order_by('title', 'id')
    else:
        users_collections = Users_Collections.objects.filter(user__id=user.id).select_related('collection').order_by('collection__title', 'collection__id')
        collections = [uc.collection for uc in users_collections]

    collection_to_course_name = getCourseNameCollectionMap()

    copy_collections = []
    for c in collections:
        course_name_short = collection_to_course_name.get(c.id, '')
        copy_collections.append({
            'id': c.id,
            'title': c.title,
            'course_name_short': course_name_short,
        })

    sorted_copy_collections = sorted(copy_collections, key=lambda c: (c['course_name_short'].lower(), c['title'].lower()))

    return sorted_copy_collections
