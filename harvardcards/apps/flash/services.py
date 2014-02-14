"""
This module contains services and commands that change the state of the system
(i.e. called for their side effects).
"""

from harvardcards.apps.flash.models import Collection

def deleteCollection(collection_id):
    """deletes a collection"""
    Collection.objects.filter(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    else:
        return False
    
