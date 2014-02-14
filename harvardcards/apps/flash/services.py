from harvardcards.apps.flash.models import Collection

def deleteCollection(collection_id):
    """delete a collection"""
    Collection.objects.filter(id=collection_id).delete()
    if not Collection.objects.filter(id=collection_id):
        return True
    else:
        return False
    
