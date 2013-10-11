from django.contrib import admin
from harvardcards.apps.flash.models import Collection, Field, Card, User, Users_Collections, Deck, Decks_Cards, Cards_Fields

admin.site.register(Collection)
admin.site.register(Field)
admin.site.register(Card)
admin.site.register(User)
admin.site.register(Users_Collections)
admin.site.register(Deck)
admin.site.register(Decks_Cards)
admin.site.register(Cards_Fields)
