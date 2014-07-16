from django.db import models
from django.contrib.auth.models import User

class Field(models.Model):
    label = models.CharField(max_length=200, blank=True)
    FIELD_TYPES = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('A', 'Audio'),
        ('V', 'Video')        
    )
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    show_label = models.BooleanField()
    display = models.BooleanField()
    sort_order = models.IntegerField()
    example_value = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.label
    def get_field_type(self):
        return self.field_type

    def export(self):
        return repr(dict(label=self.label, field_type=self.field_type, display=self.display))

class CardTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fields = models.ManyToManyField(Field, through='CardTemplates_Fields')

    def __unicode__(self):
        return self.title

class Collection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, through='Users_Collections')
    card_template = models.ForeignKey(CardTemplate)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def __unicode__(self):
        return self.title

    def export(self):
        return repr(dict(title=self.title, description=self.description))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('collectionIndex', args=[str(self.id)])

class Card(models.Model):
    DEFAULT_COLOR = "default"
    COLOR_CHOICES = (
        (DEFAULT_COLOR, "Default"),
        ("blue", "Blue"),
        ("pink", "Pink"),
        ("green", "Green"),
        ("orange", "Orange"),
        ("white", "White"),
    )
    collection = models.ForeignKey(Collection)
    sort_order = models.IntegerField()
    fields = models.ManyToManyField(Field, through='Cards_Fields')
    color = models.CharField(max_length=12, choices=COLOR_CHOICES, default=DEFAULT_COLOR)

    def __unicode__(self):
        return "Card: " + str(self.id) + "; Collection: " + str(self.collection.title)

class Deck(models.Model):
    title = models.CharField(max_length=200)
    collection = models.ForeignKey(Collection)
    cards = models.ManyToManyField(Card, through='Decks_Cards')

    def __unicode__(self):
        return self.title

    def export(self):
        return repr(dict(title=self.title, collection=self.collection.id, id=self.id))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('deckIndex', args=[str(self.id)])

class Decks_Cards(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    sort_order = models.IntegerField()

    class Meta:
        verbose_name = 'Deck Cards'
        verbose_name_plural = 'Deck Cards'
        ordering = ["sort_order"]

    def __unicode__(self):
        return "Deck: " + str(self.deck.title) + "; Card: " + str(self.card.id)

class Cards_Fields(models.Model):
    card = models.ForeignKey(Card)
    field = models.ForeignKey(Field)
    # if field.get_field_type() == 'I':
    #     value = models.FileField(upload_to='documents/%Y/%m/%d')
    # else:
    value = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Card Fields'
        verbose_name_plural = 'Card Fields'
        ordering = ['field__sort_order']

    def __unicode__(self):
        return self.value

class CardTemplates_Fields(models.Model):
    card_template = models.ForeignKey(CardTemplate)
    field = models.ForeignKey(Field)

    class Meta:
        verbose_name = 'Card Template Fields'
        verbose_name_plural = 'Card Template Fields'
        ordering = ['field__sort_order']

    def __unicode__(self):
        return "CardTemplate: " + str(self.card_template.id) + "; Field: " + str(self.field.id)

#class User(models.Model):
#    name = models.CharField(max_length=200)
#    email = models.CharField(max_length=200)
    
class Users_Collections(models.Model):
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection)
    OBSERVER = 'O'
    LEARNER = 'L'
    TEACHING_ASSISTANT = 'T'
    CONTENT_DEVELOPER = 'C'
    INSTRUCTOR = 'I'
    ADMINISTRATOR = 'A'
    ROLES = (
        (OBSERVER,              'Observer'),                  # Guest
        (LEARNER,               'Learner'),                   # Student
        (TEACHING_ASSISTANT,    'Teaching Assistant'),
        (CONTENT_DEVELOPER,     'Content Developer'),
        (INSTRUCTOR,            'Instructor'),                # Owner
        (ADMINISTRATOR,         'Administrator')
    )
    
    role_map = dict([(role[0], role[1].upper()) for role in ROLES])
    
    role = models.CharField(max_length=1, choices=ROLES, default='G')
    date_joined = models.DateField()
    class Meta:
        verbose_name = 'Users Collections'
        verbose_name_plural = 'Users Collections'

    def __unicode__(self):
        return "User: " + str(self.user.email) + " Collection: " + str(self.collection.title) + " Role: " + str(self.role)

    @classmethod
    def get_role_buckets(self, user, collections):
        ''' Given a user and a set of collections, this function returns a
        dictionary that maps roles to collections. '''

        role_buckets = dict([(bucket, []) for bucket in self.role_map.values()])
    
        user_collections = dict([
            (item.collection_id, item.role)
            for item in self.objects.filter(user=user.id)
        ])

        for collection in collections:
            if user.is_superuser:
                role = 'A'
            elif collection.id in user_collections:
                role = user_collections[collection.id]
            else:
                role = 'O'
            role_buckets[self.role_map[role]].append(collection.id)

        return role_buckets

    @classmethod
    def check_role(self, user, role, collection):
        if user.is_superuser:
            return True
        return bool(self.objects.filter(user=user.id, role=role, collection=collection.id))
