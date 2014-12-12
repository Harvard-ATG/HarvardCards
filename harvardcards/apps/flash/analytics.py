import json
import uuid
import logging
import collections

from django.utils import timezone
from django.contrib.auth.models import User
from .models import Analytics

log = logging.getLogger(__name__)

# Vocabulary of "verbs" for use in analytics statements.
# Note: uses a namedtuple instead of a dict so verbs
# can be referenced using attributes:
#
#   VERBS.reviewed => "reviewed"
#   VERBS.quizzed => "quizzed"
# 
_VERBS = {
    "viewed": "viewed",
    "quizzed": "quizzed",
    "reviewed": "reviewed",
    "launched": "launched",
    "downloaded": "downloaded",
    "created": "created",
    "modified": "modified"
}
VERBS = collections.namedtuple("VERBS", _VERBS.keys())(**_VERBS)

# Vocabulary of "objects" for use in analytics statements.
_OBJECTS = {
    "application": "application",
    "collection": "collection",
    "deck": "deck",
}
OBJECTS = collections.namedtuple("OBJECTS", _OBJECTS.keys())(**_OBJECTS)

def track(**kwargs):
    """
    Shortcut method to record a statement about a learning activity.
    Example usage:

    analytics.track(
        actor="john",
        verb=analytics.VERBS.reviewed, 
        object=analytics.OBJECTS.deck,
        context={"deck_id": 10, "mobile": True}
    )
    """
    log.debug("save statement: %s" % str(kwargs))
    model = Statement(**kwargs).save()
    return

class Statement:
    def __init__(self, *args, **kwargs):
        """
        Creates an instance of a statement.
        A statement is only valid if it has three basic parts: an actor, verb, and object.
        Raises an exception if it is missing a required part.
        """
        for required_param in ["actor", "verb", "object"]:
            if not required_param in kwargs:
                raise Exception("missing required parameter: %s" % required_param)
        
        self.id = str(uuid.uuid4())
        self.timestamp = kwargs.get('timestamp', timezone.now())
        self.verb = kwargs.get('verb', '')
        self.object = kwargs.get('object', '')
        self.context = kwargs.get('context', None)

        actor = kwargs.get('actor', None)
        if isinstance(actor, User):
            if actor.is_authenticated():
                self.actor_user = actor
                self.actor_desc = 'authenticated user'
            else:
                self.actor_user = None
                self.actor_desc = 'unauthenticated user'
        else:
            self.actor_user = None
            self.actor_desc = str(actor)

        self.analytics_model = None

    def as_dict(self):
        """Returns the object as a dictionary."""
        return {
            "id": self.id,
            "timestamp": str(self.timestamp),
            "actor_user": str(self.actor_user),
            "actor_desc": str(self.actor_desc),
            "verb": self.verb,
            "object": self.object,
            "context": self.context,
        }

    def as_json(self):
        """Returns a serialized statement in JSON format."""
        return json.dumps(self.as_dict())

    def save(self):
        """Saves the statement in a backend store."""
        x = Analytics()
        x.stmt_id = self.id
        x.stmt_timestamp = self.timestamp
        x.stmt_actor_user = self.actor_user
        x.stmt_actor_desc = self.actor_desc
        x.stmt_verb = self.verb
        x.stmt_object = self.object
        if self.context is not None:
            x.stmt_context = json.dumps(self.context)
        x.stmt_json = self.as_json()
        x.save()

        self.analytics_model = x
        log.debug("saved analytics model id: %s" % x.id)

        return self

    def __repr__(self):
        """Returns a string representation of the object."""
        return str(self.as_dict())

