from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'harvardcards.apps.flash.views.site.splash', name='splash'),
    url(r'^$', 'harvardcards.apps.flash.views.collection.index', name='index'),
    url(r'^collection/create/$', 'harvardcards.apps.flash.views.collection.create', name='collectionCreate'),
    url(r'^collection/create/(?P<collection_id>\d+)$', 'harvardcards.apps.flash.views.collection.create', name='collectionCreate'),
    url(r'^collection/$', 'harvardcards.apps.flash.views.collection.index', name='collection_id'),
    url(r'^collection/(?P<collection_id>\d+)$', 'harvardcards.apps.flash.views.collection.index', name='collection_id'),
    url(r'^collection/(?P<collection_id>\d+)/upload', 'harvardcards.apps.flash.views.collection.upload_deck', name='collectionUploadDeck'),
    url(r'^collection/(?P<collection_id>\d+)/download-template', 'harvardcards.apps.flash.views.collection.download_template', name='collectionDownloadTemplate'),

    url(r'^deck/create/$', 'harvardcards.apps.flash.views.deck.create', name='createDeck'),
    url(r'^deck/delete/$', 'harvardcards.apps.flash.views.deck.delete', name='deleteDeck'),
    url(r'^deck/$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)$', 'harvardcards.apps.flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)/download$', 'harvardcards.apps.flash.views.deck.download_deck', name='deckDownload'),
    url(r'^deck/test1/$', 'harvardcards.apps.flash.views.deck.test1', name='deckIndex'),
    url(r'^deck/test2/$', 'harvardcards.apps.flash.views.deck.test2', name='deckIndex'),
    url(r'^card/create/$', 'harvardcards.apps.flash.views.card.create', name='createCard'),
    url(r'^card/fields/$', 'harvardcards.apps.flash.views.card.fields', name='cardFields'),
    url(r'^card/delete/$', 'harvardcards.apps.flash.views.card.delete', name='deleteCard'),
    url(r'^card/fieldEdit/$', 'harvardcards.apps.flash.views.card.fieldEdit', name='editCardField'),
    
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    
    # API
    url(r'^collection/fields/$', 'harvardcards.apps.flash.views.api.collection.fields', name='fieldsCollection'),
    url(r'^collection/delete/$', 'harvardcards.apps.flash.views.api.collection.delete', name='deleteCollection'),
    
	
	# url(r'^$', 'HarvardCards.views.home', name='home'),
    # url(r'^HarvardCards/', include('harvardcards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the jasmine test runner:
    url(r'^jasmine/', include('harvardcards.apps.jasmine.urls'))
)
