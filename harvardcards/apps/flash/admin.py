from django.contrib import admin
from harvardcards.apps.flash.models import Collection, Field, Card, User, Users_Collections, Deck, Decks_Cards, Cards_Fields
from harvardcards.apps.flash.forms import *

class CardsInLine(admin.StackedInline):
    model = Cards_Fields
    extra = 1
    max_num = 1

class DecksInLine(admin.StackedInline):
    model = Decks_Cards
    extra = 1
    max_num = 1

class CardAdmin(admin.ModelAdmin):
    inlines=(CardsInLine, DecksInLine)

admin.site.register(Collection)
admin.site.register(Field)
admin.site.register(Card, CardAdmin)
admin.site.register(User)
admin.site.register(Users_Collections)
admin.site.register(Deck)
admin.site.register(Decks_Cards)
admin.site.register(Cards_Fields)
