from functools import wraps

from django.core.exceptions import PermissionDenied
from harvardcards.apps.flash.models import Deck
from harvardcards.apps.flash.services import has_role_with_request

def check_role(roles, entity_type):
    """
    A decorator that checks to see if a user has the required role in a collection. 
    Allows the user to enter the function if the user has the role. 
    
    Raises a PermissionDenied exception if the user doesn't have the role.

    Input: a list of roles allowed for this function
    Output: the function if user has role, else a PermissionDenied
    """
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            entity_id = None
            if request.GET:
                entity_id = request.GET.get('deck_id','') if entity_type == 'deck' else request.GET.get('collection_id','')
            elif not entity_id and request.POST:
                entity_id = request.POST.get('deck_id','') if entity_type == 'deck' else request.POST.get('collection_id','')
            else:
                raise PermissionDenied
            
            entity_id = int(entity_id)
            if entity_type == 'deck':
                deck = Deck.objects.get(id=entity_id)
                entity_id = deck.collection.id
            
            if has_role_with_request(request, roles, entity_id):
                return func(request, *args, **kwargs)
            raise PermissionDenied
        return wraps(func)(inner_decorator)
    return decorator

