from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'harvardcards.apps.flash.views.site.splash', name='splash'),
    url(r'^$', 'harvardcards.apps.flash.views.collection.index', name='index'),

    url(r'^collection$', 'harvardcards.apps.flash.views.collection.index', name='collectionIndex'),

    url(r'^collection/create$', 'harvardcards.apps.flash.views.collection.create', name='collectionCreate'),
    url(r'^collection/(?P<collection_id>\d+)$', 'harvardcards.apps.flash.views.collection.index', name='collectionIndex'),
    url(r'^collection/(?P<collection_id>\d+)/add-deck$', 'harvardcards.apps.flash.views.collection.add_deck', name='collectionAddDeck'),
    url(r'^collection/(?P<collection_id>\d+)/edit$', 'harvardcards.apps.flash.views.collection.edit', name='collectionEdit'),
    url(r'^collection/(?P<collection_id>\d+)/download-template', 'harvardcards.apps.flash.views.collection.download_template', name='collectionDownloadTemplate'),
    url(r'^collection/(?P<collection_id>\d+)/delete', 'harvardcards.apps.flash.views.collection.delete', name='collectionDelete'),
    url(r'collection/(?P<collection_id>\d+)/share', 'harvardcards.apps.flash.views.collection.share_collection', name='collectionShare'),
    url(r'collection/share/(?P<secret_share_key>.*)', 'harvardcards.apps.flash.views.collection.add_user_to_shared_collection', name='collectionShareValidate'),
    url(r'^card_template/preview$', 'harvardcards.apps.flash.views.card_template.preview', name='cardTemplatePreview'),

    url(r'^deck$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)/edit$', 'harvardcards.apps.flash.views.deck.index', name='deckEdit'),
    url(r'^deck/(?P<deck_id>\d+)/create-card', 'harvardcards.apps.flash.views.deck.create_edit_card', name='deckCreateCard'),
    url(r'^deck/(?P<deck_id>\d+)/edit-card', 'harvardcards.apps.flash.views.deck.create_edit_card', name='deckEditCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete-card', 'harvardcards.apps.flash.views.deck.delete_card', name='deckDeleteCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete', 'harvardcards.apps.flash.views.deck.delete', name='deckDelete'),
    url(r'^deck/(?P<deck_id>\d+)/download$', 'harvardcards.apps.flash.views.deck.download_deck', name='deckDownload'),
    url(r'^deck/(?P<deck_id>\d+)/upload$', 'harvardcards.apps.flash.views.deck.upload_deck', name='deckUpload'),
    
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # API
    url(r'^api$', 'harvardcards.apps.flash.api.api.root', name='apiRoot'),
    url(r'^api/card/edit', 'harvardcards.apps.flash.api.card.edit', name='apiCardEdit'),
    url(r'^api/card/delete$', 'harvardcards.apps.flash.api.card.delete', name='apiCardDelete'),
    url(r'^api/deck/rename$', 'harvardcards.apps.flash.api.deck.rename', name='apiDeckRename'),
    url(r'^api/deck/delete$', 'harvardcards.apps.flash.api.deck.delete', name='apiDeckDelete'),
    url(r'^api/collection/fields$', 'harvardcards.apps.flash.api.collection.fields', name='apiCollectionFields'),
    url(r'^api/collection/delete$', 'harvardcards.apps.flash.api.collection.delete', name='apiCollectionDelete'),
    
	# url(r'^$', 'HarvardCards.views.home', name='home'),
    # url(r'^HarvardCards/', include('harvardcards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the jasmine test runner:
    url(r'^jasmine/', include('harvardcards.apps.jasmine.urls'))
)
