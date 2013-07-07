from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=200)
    decription = models.CharField(max_length=4000)

class Card(models.Model):
    collection_id = models.IntegerField()

class CollectionsCard(models.Model):
    collection_id = models.ForeignKey(Collection)
    card_id = models.ForeignKey(Card)
    sort_order = models.IntegerField()
    
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class CollectionsUser(models.Model):
    collection_id = models.ForeignKey(Collection)
    user_id = models.ForeignKey(User)

class Deck(models.Model):
    title = models.CharField(max_length=200)
    collection_id = models.ForeignKey(Collection)
    owner_id = models.ForeignKey(User)

class DecksCard(models.Model):
    deck_id = models.ForeignKey(Deck)
    card_id = models.ForeignKey(Card)
    sort_order = models.IntegerField()

class Field(models.Model):
    label = models.CharField(max_length=200)
    FIELD_TYPES = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('A', 'Audio'),
        ('V', 'Video')        
    )
    field_type = models.CharField(max_length = 1, choices = FIELD_TYPES)
    show_label = models.BooleanField()
    collection_id = models.ForeignKey(Collection)
    display = models.BooleanField()

class CardsField(models.Model):
    card_id = models.ForeignKey(Card)
    field_id = models.ForeignKey(Field)
