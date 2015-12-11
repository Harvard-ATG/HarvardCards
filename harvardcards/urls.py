from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from flash.views.lti import LTILaunchView, ToolConfigView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from flash.views import collection as collection_views
from flash.views import deck as deck_views
from flash.views import card_template as card_template_views
import flash.views
import flash.views.site
import flash.views.stats_graph
import django.views.static
import flash.api.api
import flash.api.card
import flash.api.deck
import flash.api.collection
import flash.api.analytics




urlpatterns = [
    #url(r'^$', 'flash.views.site.splash', name='splash'),
    url(r'^$', collection_views.index, name='index'),

    # collection urls
    url(r'^collection$', collection_views.index, name='collectionIndex'),
    url(r'^collection/custom', collection_views.custom_create, name='collectionCustom'),
    url(r'^collection/create$', collection_views.create, name='collectionCreate'),
    url(r'^collection/copy', collection_views.copy_collection, name='collectionCopy'),
    url(r'^collection/(?P<collection_id>\d+)$', collection_views.index, name='collectionIndex'),
    url(r'^collection/(?P<collection_id>\d+)/add-deck$', collection_views.add_deck, name='collectionAddDeck'),
    url(r'^collection/custom/upload', collection_views.custom_create, name='customDeckUpload'),
    url(r'^collection/(?P<collection_id>\d+)/edit$', collection_views.edit, name='collectionEdit'),
    url(r'^collection/(?P<collection_id>\d+)/publish$', collection_views.toggle_publish, name='collectionPublish'),

    url(r'^collection/(?P<collection_id>\d+)/all_cards$', deck_views.all_cards, name='allCards'),
    url(r'^collection/(?P<collection_id>\d+)/delete-card', deck_views.delete_card_collection, name='collectionDeleteCard'),
    url(r'^collection/(?P<collection_id>\d+)/edit-card', deck_views.edit_card_collection, name='collectionEditCard'),

    url(r'^collection/(?P<collection_id>\d+)/download-template', collection_views.download_template, name='collectionDownloadTemplate'),
    url(r'^collection/download-custom-template', collection_views.download_custom_template, name='collectionDownloadCustomTemplate'),
    url(r'^collection/(?P<collection_id>\d+)/delete', collection_views.delete, name='collectionDelete'),
    url(r'^collection/(?P<collection_id>\d+)/share', collection_views.share_collection, name='collectionShare'),
    url(r'^collection/share/(?P<secret_share_key>.*)', collection_views.add_user_to_shared_collection, name='collectionShareValidate'),
    url(r'^card_template/preview$', card_template_views.preview, name='cardTemplatePreview'),

    # deck urls
    url(r'^deck$', deck_views.index, name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)$', deck_views.index, name='deckIndex'),
    url(r'^deck/(?P<deck_id>\d+)/edit$', deck_views.index, name='deckEdit'),
    url(r'^deck/(?P<deck_id>\d+)/create-card', deck_views.create_edit_card, name='deckCreateCard'),
    url(r'^deck/(?P<deck_id>\d+)/edit-card', deck_views.create_edit_card, name='deckEditCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete-card', deck_views.delete_card, name='deckDeleteCard'),
    url(r'^deck/(?P<deck_id>\d+)/delete', deck_views.delete, name='deckDelete'),
    url(r'^deck/(?P<deck_id>\d+)/download$', deck_views.download_deck, name='deckDownload'),
    url(r'^deck/(?P<deck_id>\d+)/upload$', deck_views.upload_deck, name='deckUpload'),

    # logout
    url(r'^logout', django.contrib.auth.views.logout, {'next_page': '/'}, name='logout'),

    # media files
    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

    # admin graphs
    url(r'stats_graphs$', flash.views.stats_graph.graphs, name='stats_graphs'),

    # help file
    url(r'^help$', flash.views.site.help, name='help'),

    # lti launch & configuration
    url(r'^lti_launch$', LTILaunchView.as_view(), name='lti-launch'),
    url(r'^lti_tool_config$', ToolConfigView.as_view(), name='lti-tool-config'),

    # API
    url(r'^api$', flash.api.api.root, name='apiRoot'),
    url(r'^api/card/edit', flash.api.card.edit, name='apiCardEdit'),
    url(r'^api/card/delete$', flash.api.card.delete, name='apiCardDelete'),
    url(r'^api/deck/rename$', flash.api.deck.rename, name='apiDeckRename'),
    url(r'^api/deck/delete$', flash.api.deck.delete, name='apiDeckDelete'),
    url(r'^api/collection/fields$', flash.api.collection.fields, name='apiCollectionFields'),
    url(r'^api/collection/delete$', flash.api.collection.delete, name='apiCollectionDelete'),
    url(r'^api/analytics/track$', flash.api.analytics.track, name='apiAnalyticsTrack'),

	# url(r'^$', 'HarvardCards.views.home', name='home'),
    # url(r'^HarvardCards/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the next line to enable the jasmine test runner:
    url(r'^jasmine/', include('jasmine.urls'))
]
