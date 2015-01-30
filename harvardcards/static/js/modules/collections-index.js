define(['jquery','views/CollectionListView','views/CollectionCreateModal'], function($,CollectionListView, CollectionCreateModal) {

    return {
		initModule: function(){
		    var collection_list_view = new CollectionListView({
		        headerSelector: ".courseHeader",
		        btnSelector: "#expandCollapseAllBtn"
		    });

		    var collection_create_modal = new CollectionCreateModal({
		        btnSelector: "#addAcourse",
		        dialogSelector: "#addAcourseDialog"
		    });

			collection_list_view.init();
			collection_create_modal.init();
		}
	};
});
