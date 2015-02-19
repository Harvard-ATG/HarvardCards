from django.contrib import admin
from harvardcards.apps.flash.models import *
from django.contrib.auth.models import User

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
    list_display = ('title', 'collection', 'sort_order')
    inlines=(CardsInLine,)
    ordering = ('collection','sort_order', 'title')

class UsersInLine(admin.StackedInline):
    extra = 0
    verbose_name = 'User'
    model = Users_Collections

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'card_template')
    inlines = (UsersInLine,)

class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'stmt_stored', 'stmt_actor_user', 'stmt_actor_desc', 'stmt_verb', 'stmt_object', 'stmt_context')
    search_fields=('stmt_actor_user__username', 'stmt_verb', 'stmt_object')

class CloneAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'model_id', 'status', 'clone_date', 'cloned_by')
    search_fields=('cloned_by__username', 'model_id', 'status')
    ordering = ('-clone_date', 'model', 'model_id', 'cloned_by', 'status')

class ClonedAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'old_model_id', 'new_model_id')
    ordering = ('model', 'old_model_id', 'new_model_id')

class MediaStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_md5hash', 'file_type', 'file_size', 'store_created', 'store_updated', 'reference_count')

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Field)
admin.site.register(Card, CardAdmin)
admin.site.register(Users_Collections)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Decks_Cards)
admin.site.register(Cards_Fields)
admin.site.register(CardTemplate)
admin.site.register(CardTemplates_Fields)
admin.site.register(Canvas_Course_Map)
admin.site.register(Canvas_Course)
admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(Clone, CloneAdmin)
admin.site.register(Cloned, ClonedAdmin)
admin.site.register(MediaStore, MediaStoreAdmin)
