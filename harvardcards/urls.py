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
    url(r'^collection/(?P<collection_id>\d+)/edit$', 'harvardcards.apps.flash.views.collection.edit', name='collectionEdit'),
    url(r'^collection/(?P<collection_id>\d+)/upload', 'harvardcards.apps.flash.views.collection.upload_deck', name='collectionUploadDeck'),
    url(r'^collection/(?P<collection_id>\d+)/download-template', 'harvardcards.apps.flash.views.collection.download_template', name='collectionDownloadTemplate'),
    url(r'^collection/(?P<collection_id>\d+)/delete', 'harvardcards.apps.flash.views.collection.delete', name='collectionDelete'),

    url(r'^card_template/preview$', 'harvardcards.apps.flash.views.card_template.preview', name='cardTemplatePreview'),

    url(r'^deck$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)/edit$', 'harvardcards.apps.flash.views.deck.edit', name='deckEdit'),
    url(r'^deck/(?P<deck_id>\d+)/delete$', 'harvardcards.apps.flash.views.deck.delete', name='deckDelete'),
    url(r'^deck/(?P<deck_id>\d+)/download$', 'harvardcards.apps.flash.views.deck.download_deck', name='deckDownload'),
    
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # API
    # Commenting these out because they aren't being used for anything yet
    #url(r'^collection/fields/$', 'harvardcards.apps.flash.views.api.collection.fields', name='fieldsCollection'),
    #url(r'^collection/delete/$', 'harvardcards.apps.flash.views.api.collection.delete', name='deleteCollection'),
    url(r'^api/card/create$', 'harvardcards.apps.flash.api.card.create', name='apiCardCreate'),
    url(r'^api/card/delete$', 'harvardcards.apps.flash.api.card.delete', name='apiCardDelete'),
    
	# url(r'^$', 'HarvardCards.views.home', name='home'),
    # url(r'^HarvardCards/', include('harvardcards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the jasmine test runner:
    url(r'^jasmine/', include('harvardcards.apps.jasmine.urls'))
)