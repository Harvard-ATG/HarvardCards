from django.contrib import admin
from harvardcards.apps.flash.models import Collection, Field, Card, User, Users_Collections, Deck, Decks_Cards, Cards_Fields

class CardsInLine(admin.StackedInline):
    verbose_name = "Card's fields"
    model = Cards_Fields
    extra = 0

class DecksInLine(admin.StackedInline):
    model = Decks_Cards
    extra = 0

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'collection',)
    search_fields=('collection__title', )
    inlines=(DecksInLine, CardsInLine,)


class CardsInLine(admin.StackedInline):
    extra=0
    verbose_name = 'Card'
    model=Decks_Cards

class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'collection')
    inlines=(CardsInLine,)

admin.site.register(Collection)
admin.site.register(Field)
admin.site.register(Card, CardAdmin)
admin.site.register(User)
admin.site.register(Users_Collections)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Decks_Cards)
admin.site.register(Cards_Fields)
