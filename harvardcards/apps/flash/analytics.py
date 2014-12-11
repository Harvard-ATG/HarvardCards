import datetime
import json
import uuid
import logging
import collections

from .models import Analytics

log = logging.getLogger(__name__)

_VERBS = {
    "accessed": "accessed",
    "quizzed": "quizzed",
    "reviewed": "reviewed",
    "launched": "launched",
    "downloaded": "downloaded"
}

VERBS = collections.namedtuple("VERBS", _VERBS.keys())(**_VERBS)

def save_statement(**kwargs):
    """
    Shortcut method to record a statement about a learning activity.
    Example usage:

    analytics.save_statement(
        actor="John", 
        verb="reviewed", 
        object="latin flashcards",
        context={"mobile": False}
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
        self.timestamp = kwargs.get('timestamp', datetime.datetime.now())
        self.actor = kwargs.get('actor', None)
        self.verb = kwargs.get('verb', '')
        self.object = kwargs.get('object', '')
        self.context = kwargs.get('context', None)
        self.analytics_model = None

    def as_dict(self):
        """Returns the object as a dictionary."""
        return {
            "id": self.id,
            "timestamp": str(self.timestamp),
            "actor": str(self.actor),
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
        x.stmt_actor = self.actor
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

