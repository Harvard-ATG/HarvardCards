from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.urlresolvers import reverse

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
    sort_order = models.IntegerField(default=1)
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
    owner = models.ForeignKey(User, blank=True, null=True)
    def __unicode__(self):
        return self.title

class Collection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, through='Users_Collections')
    card_template = models.ForeignKey(CardTemplate)
    published = models.BooleanField(default=True)

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

    def get_all_cards_url(self):
        from django.core.urlresolvers import reverse
        return reverse('allCards', args=[str(self.id)])

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
    sort_order = models.IntegerField(default=1)
    fields = models.ManyToManyField(Field, through='Cards_Fields')
    color = models.CharField(max_length=12, choices=COLOR_CHOICES, default=DEFAULT_COLOR)
    clone_ref_id = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return "Card: " + str(self.id) + "; Collection: " + str(self.collection.title)

class Deck(models.Model):
    title = models.CharField(max_length=200)
    collection = models.ForeignKey(Collection)
    cards = models.ManyToManyField(Card, through='Decks_Cards')
    sort_order = models.IntegerField(default=1)
    clone_ref_id = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = 'Deck'
        verbose_name_plural = 'Decks'
        ordering = ["sort_order","title"]

    def __unicode__(self):
        return self.title

    def export(self):
        return repr(dict(title=self.title, collection=self.collection.id, id=self.id))

    def get_absolute_url(self):
        return reverse('deckIndex', args=[str(self.id)])

    def get_add_card_url(self):
        return reverse('deckCreateCard', args=[str(self.id)])


class Decks_Cards(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    sort_order = models.IntegerField(default=1)
    clone_ref_id = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = 'Deck Cards'
        verbose_name_plural = 'Deck Cards'
        ordering = ["sort_order"]

    def __unicode__(self):
        return "Deck: " + str(self.deck.title) + "; Card: " + str(self.card.id)

class Cards_Fields(models.Model):
    card = models.ForeignKey(Card)
    field = models.ForeignKey(Field)
    value = models.CharField(max_length=500)
    clone_ref_id = models.CharField(max_length=50, null=True)

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

class Users_Collections(models.Model):

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
        (ADMINISTRATOR,         'Administrator'))

    role_map = dict([(role[0], role[1].upper().replace(" ", "_")) for role in ROLES])

    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection)
    date_joined = models.DateField()
    role = models.CharField(max_length=1, choices=ROLES, default='O')
    
    class Meta:
        verbose_name = 'Users Collections'
        verbose_name_plural = 'Users Collections'

    def __unicode__(self):
        return "User: " + str(self.user.email) + " Collection: " + str(self.collection.title) + " Role: " + str(self.role)

    @classmethod
    def is_valid_role(self, role):
        '''
        Returns true if the given role is valid, otherwise false.

        Note: the role parameter can be a string or tuple:
            role='A' 
            role=('A','Administrator')

        Both are equivalent and should return true.
        '''
        if not isinstance(role, basestring):
            return role[0] in self.role_map
        return role in self.role_map

    @classmethod
    def get_role_buckets(self, user, collections = None):
        ''' Given a user and a set of collections, this function returns a
        dictionary that maps roles to collections. '''

        role_buckets = dict([(bucket, []) for bucket in self.role_map.values()])
        
        if not collections:
            collections = Collection.objects.only('id')

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

class Course(models.Model):
    """
    Course information. 
    """
    canvas_course_id = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.CharField(max_length=255, unique=True, blank=False)
    entity =  models.CharField(max_length=255, blank=False)
    context_id = models.CharField(max_length=255, blank=False)
    course_name_short = models.CharField(max_length=1024)
    course_name = models.CharField(max_length=2048)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses '
        ordering = ['course_id','course_name_short','course_name']

    def __unicode__(self):
        return "Course %s - %s" % (self.course_id, self.course_name_short)


class Course_Map(models.Model):
    """
    The purpose of this model is to setup a many-to-many mapping between 
    Canvas courses and collections.
    """
    course = models.ForeignKey(Course)
    collection = models.ForeignKey(Collection)
    subscribe = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Course Map'
        verbose_name_plural = 'Course Maps'
        ordering = ['course','collection__id','subscribe']

    def __unicode__(self):
        return "course: " + str(self.course) + " Collection id: " + str(self.collection.id)

class Analytics(models.Model):
    stmt_id = models.CharField(max_length=36, blank=False)
    stmt_actor_user = models.ForeignKey(User, null=True)
    stmt_actor_desc = models.CharField(max_length=4000, blank=False)
    stmt_verb = models.CharField(max_length=4000, blank=False)
    stmt_object = models.CharField(max_length=4000, blank=False)
    stmt_context = models.TextField(blank=True)
    stmt_timestamp = models.DateTimeField(default=datetime.datetime.now)
    stmt_stored = models.DateTimeField(auto_now_add=True)
    stmt_json = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'
        ordering = ['-stmt_stored', 'stmt_actor_user', 'stmt_actor_desc', 'stmt_verb', 'stmt_object']

    def __unicode__(self):
        return "ID: %s STMT: %s-%s-%s-%s" % (self.id, self.stmt_actor_user, self.stmt_actor_desc, self.stmt_verb, self.stmt_object)

class Clone(models.Model):
    CLONE_STATUS = (
        ('Q', 'QUEUED'),
        ('P', 'PROCESSING'),
        ('D', 'DONE')
    )
    clone_date = models.DateTimeField(auto_now_add=True)
    cloned_by = models.ForeignKey(User)
    model = models.CharField(max_length=48, null=False)
    model_id = models.CharField(max_length=24, null=False)
    status = models.CharField(max_length=1, choices=CLONE_STATUS)

    class Meta:
        verbose_name = 'Clone'
        verbose_name_plural = 'Clones'
        ordering = ['-clone_date', 'model', 'model_id', 'cloned_by']

    def __unicode__(self):
        return "Clone: " + str(self.model) + " " + str(self.model_id) + " [" + str(self.status) + "]"

class Cloned(models.Model):
    clone = models.ForeignKey(Clone)
    model = models.CharField(max_length=48, null=False)
    old_model_id = models.CharField(max_length=24, null=False)
    new_model_id = models.CharField(max_length=24, null=False)

    class Meta:
        verbose_name = 'Cloned'
        verbose_name_plural = 'Cloned'
        ordering = ['-clone', 'model', 'old_model_id', 'new_model_id']

    def __unicode__(self):
        return "Cloned: " + str(self.model) + " OLD: " + str(self.old_model_id) + " NEW: " + str(self.new_model_id)

class MediaStore(models.Model):
    file_name = models.CharField(max_length=1024, null=False)
    file_size = models.PositiveIntegerField(null=False)
    file_type = models.CharField(max_length=127, null=False)
    file_md5hash = models.CharField(max_length=32, null=False)
    store_created = models.DateTimeField(auto_now_add=True)
    store_updated = models.DateTimeField(auto_now=True)
    reference_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Media Store'
        verbose_name_plural = 'Media Stores'
        ordering = ['file_name']

    def __unicode__(self):
        return "MediaStore: " + str(self.file_name) + " HASH: " + str(self.file_md5hash)
