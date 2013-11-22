from django.db import models

class Collection(models.Model):
    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title
    description = models.TextField(blank=True)
    #users = models.ManyToManyField(User, through='UserCollection')
    def export(self):
        return repr(dict(title=self.title, description=self.description))

class Field(models.Model):
    label = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return self.label
    FIELD_TYPES = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('A', 'Audio'),
        ('V', 'Video')        
    )
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    show_label = models.BooleanField()
    collection = models.ForeignKey(Collection)
    display = models.BooleanField()
    sort_order = models.IntegerField()
    def export(self):
        return repr(dict(label=self.label, field_type=self.field_type, sort_order=self.sort_order, display=self.display))

class Card(models.Model):

    collection = models.ForeignKey(Collection)
    sort_order = models.IntegerField(verbose_name="Card ID")
    fields = models.ManyToManyField(Field, through='Cards_Fields')
    def __unicode__(self):
        name = "Card: "+ str(self.sort_order) +"; Collection: "+ str(self.collection.title)
        return name
    
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    collections = models.ManyToManyField(Collection, through='Users_Collections')

class Users_Collections(models.Model):
    class Meta:
        verbose_name = 'Users Collection'

    collection = models.ForeignKey(Collection)
    user = models.ForeignKey(User)
    PERMISSIONS = (
        ('G', 'Guest'),
        ('S', 'Student'),
        ('A', 'Admin'),
        ('O', 'Owner')
    )
    permission = models.CharField(max_length=1, choices=PERMISSIONS, default='G')

class Deck(models.Model):
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title
    collection = models.ForeignKey(Collection)
    #owner = models.ForeignKey(User)
    cards = models.ManyToManyField(Card, through='Decks_Cards')
    def export(self):
        return repr(dict(title=self.title, collection=self.collection.id, id=self.id))

class Decks_Cards(models.Model):
    class Meta:
        verbose_name = 'Choose Deck'
        verbose_name_plural = 'Choose Deck'
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    sort_order = models.IntegerField()
    def __unicode__(self):
        name="Deck: "+str(self.deck.title) +"; Card: "+ str(self.card.sort_order)
        return name

class Cards_Fields(models.Model):
    class Meta:
        verbose_name = 'Card Fields'
        verbose_name_plural = 'Card Fields'

    value = models.CharField(max_length=500)
    card = models.ForeignKey(Card)
    field = models.ForeignKey(Field)
    sort_order = models.IntegerField()
    def __unicode__(self):
        return self.value