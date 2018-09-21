from django.contrib import admin
from flash.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserAdminCustom(UserAdmin):
    list_display = ( UserAdmin.list_display[0], 'num_collections', UserAdmin.list_display[-1])
    def num_collections(self, obj):
        return Users_Collections.objects.filter(user=obj).count()

    def queryset(self, request):
        return User.objects.extra(
            select={'num_collections': "select count(*) from flash_users_collections where flash_users_collections.user_id = auth_user.id"},
            )
    num_collections.admin_order_field = 'num_collections'
    num_collections.short_description = 'Number of Collections'

class FieldAdmin(admin.ModelAdmin):
    model = Field
    list_display = ('label', 'field_type', 'show_label', 'display', 'sort_order', 'example_value')

class FieldsInline(admin.StackedInline):
    model = Field

class CardTemplatesFieldsInline(admin.StackedInline):
    model = CardTemplates_Fields
    inlines = (FieldsInline,)

class CardTemplateAdmin(admin.ModelAdmin):
    model = CardTemplate
    inlines = (CardTemplatesFieldsInline,)

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

class UsersCollectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'collection', 'role', 'date_joined')
    search_fields = ('user__email', 'collection__title', 'role')
    ordering = ('-date_joined',)

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


class CollectionsInLine(admin.StackedInline):
    extra = 0
    verbose_name = 'Collections'
    model = Course_Map

class CourseAdmin(admin.ModelAdmin):
    inlines = (CollectionsInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Users_Collections, UsersCollectionsAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Decks_Cards)
admin.site.register(Cards_Fields)
admin.site.register(CardTemplate, CardTemplateAdmin)
admin.site.register(CardTemplates_Fields)
admin.site.register(Course_Map)
admin.site.register(Course, CourseAdmin)
admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(Clone, CloneAdmin)
admin.site.register(Cloned, ClonedAdmin)
admin.site.register(MediaStore, MediaStoreAdmin)
