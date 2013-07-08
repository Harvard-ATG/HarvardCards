from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=200)
    decription = models.CharField(max_length=4000)
    #users = models.ManyToManyField(User, through='UserCollection')

class Field(models.Model):
    label = models.CharField(max_length=200)
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

class Card(models.Model):
    collection = models.ForeignKey(Collection)
    sort_order = models.IntegerField()
    fields = models.ManyToManyField(Field, through='Cards_Fields')
    
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    collections = models.ManyToManyField(Collection, through='Users_Collections')

class Users_Collections(models.Model):
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
    collection = models.ForeignKey(Collection)
    owner = models.ForeignKey(User)
    cards = models.ManyToManyField(Card, through='Decks_Cards')

class Decks_Cards(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    sort_order = models.IntegerField()

class Cards_Fields(models.Model):
    card = models.ForeignKey(Card)
    field = models.ForeignKey(Field)
    sort_order = models.IntegerField()