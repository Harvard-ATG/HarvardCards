define(['jquery','views/CollectionListView','views/CollectionCreateModal', 'views/DeckCreateModal'], function($,CollectionListView, CollectionCreateModal, DeckCreateModal) {
    document.getElementById('collection_type').onchange = function(){
        var currentVal = this.value;
        if (currentVal == 2){
            $('#course_coll').show();
            $('#private_coll').hide();
        }
        else if (currentVal == 3){
            $('#course_coll').hide();
            $('#private_coll').show();
        }
        else{
            $('#course_coll').show();
            $('#private_coll').show();
        }
    }
    return {
		initModule: function(){
		    var collection_list_view = new CollectionListView({
		        headerSelector: ".courseHeaderClickable",
		        btnSelector: "#expandCollapseAllBtn"
		    });

		    var collection_create_modal = new CollectionCreateModal({
		        btnSelector: "#addAcourse",
		        dialogSelector: "#addAcourseDialog"
		    });

			collection_list_view.init();
			collection_create_modal.init();

            var deck_modals = [];
            var collections = $('[data-collection-id]')
            for (var i = 0; i < collections.length; ++i) {
                var collection = collections[i]
                var collection_id = $(collection).data('collection-id')

                deck_modals[i] = new DeckCreateModal({
                    btnSelector: "#addDeck-"+collection_id,
                    dialogSelector: "#addAdeckDialog-"+collection_id,
                    form_name: "form-"+collection_id
                });

                deck_modals[i].init();
            }

		}
	};
});
