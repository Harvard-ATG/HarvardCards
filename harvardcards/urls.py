from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from flash.views.lti import LTILaunchView, ToolConfigView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'flash.views.site.splash', name='splash'),
    url(r'^$', 'flash.views.collection.index', name='index'),

    # collection urls
    url(r'^collection$', 'flash.views.collection.index', name='collectionIndex'),
    url(r'^collection/custom', 'flash.views.collection.custom_create', name='collectionCustom'),
    url(r'^collection/create$', 'flash.views.collection.create', name='collectionCreate'),
    url(r'^collection/copy', 'flash.views.collection.copy_collection', name='collectionCopy'),
    url(r'^collection/(?P<collection_id>\d+)$', 'flash.views.collection.index', name='collectionIndex'),
    url(r'^collection/(?P<collection_id>\d+)/add-deck$', 'flash.views.collection.add_deck', name='collectionAddDeck'),
    url(r'^collection/custom/upload', 'flash.views.collection.custom_create', name='customDeckUpload'),
    url(r'^collection/(?P<collection_id>\d+)/edit$', 'flash.views.collection.edit', name='collectionEdit'),
    url(r'^collection/(?P<collection_id>\d+)/publish$', 'flash.views.collection.toggle_publish', name='collectionPublish'),

    url(r'^collection/(?P<collection_id>\d+)/all_cards$', 'flash.views.deck.all_cards', name='allCards'),
    url(r'^collection/(?P<collection_id>\d+)/delete-card', 'flash.views.deck.delete_card_collection', name='collectionDeleteCard'),
    url(r'^collection/(?P<collection_id>\d+)/edit-card', 'flash.views.deck.edit_card_collection', name='collectionEditCard'),

    url(r'^collection/(?P<collection_id>\d+)/download-template', 'flash.views.collection.download_template', name='collectionDownloadTemplate'),
    url(r'^collection/download-custom-template', 'flash.views.collection.download_custom_template', name='collectionDownloadCustomTemplate'),
    url(r'^collection/(?P<collection_id>\d+)/delete', 'flash.views.collection.delete', name='collectionDelete'),
    url(r'^collection/(?P<collection_id>\d+)/share', 'flash.views.collection.share_collection', name='collectionShare'),
    url(r'^collection/share/(?P<secret_share_key>.*)', 'flash.views.collection.add_user_to_shared_collection', name='collectionShareValidate'),
    url(r'^card_template/preview$', 'flash.views.card_template.preview', name='cardTemplatePreview'),

    # deck urls
    url(r'^deck$', 'flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)$', 'flash.views.deck.index', name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)/edit$', 'flash.views.deck.index', name='deckEdit'),
    url(r'^deck/(?P<deck_id>\d+)/create-card', 'flash.views.deck.create_edit_card', name='deckCreateCard'),
    url(r'^deck/(?P<deck_id>\d+)/edit-card', 'flash.views.deck.create_edit_card', name='deckEditCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete-card', 'flash.views.deck.delete_card', name='deckDeleteCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete', 'flash.views.deck.delete', name='deckDelete'),
    url(r'^deck/(?P<deck_id>\d+)/download$', 'flash.views.deck.download_deck', name='deckDownload'),
    url(r'^deck/(?P<deck_id>\d+)/upload$', 'flash.views.deck.upload_deck', name='deckUpload'),
    
    # logout
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    
    # media files
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # admin graphs
    url(r'stats_graphs$', 'flash.views.stats_graph.graphs', name='stats_graphs'),
                       
    # help file
    url(r'^help$', 'flash.views.site.help', name='help'),

    # lti launch & configuration
    url(r'^lti_launch$', LTILaunchView.as_view(), name='lti-launch'),
    url(r'^lti_tool_config$', ToolConfigView.as_view(), name='lti-tool-config'),

    # API
    url(r'^api$', 'flash.api.api.root', name='apiRoot'),
    url(r'^api/card/edit', 'flash.api.card.edit', name='apiCardEdit'),
    url(r'^api/card/delete$', 'flash.api.card.delete', name='apiCardDelete'),
    url(r'^api/deck/rename$', 'flash.api.deck.rename', name='apiDeckRename'),
    url(r'^api/deck/delete$', 'flash.api.deck.delete', name='apiDeckDelete'),
    url(r'^api/collection/fields$', 'flash.api.collection.fields', name='apiCollectionFields'),
    url(r'^api/collection/delete$', 'flash.api.collection.delete', name='apiCollectionDelete'),
    url(r'^api/analytics/track$', 'flash.api.analytics.track', name='apiAnalyticsTrack'),
    
	# url(r'^$', 'HarvardCards.views.home', name='home'),
    # url(r'^HarvardCards/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the jasmine test runner:
    url(r'^jasmine/', include('jasmine.urls'))
)
