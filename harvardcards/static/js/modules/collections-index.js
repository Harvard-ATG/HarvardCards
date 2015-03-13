define(['jquery','views/CollectionListView','views/CollectionCreateModal'], function($,CollectionListView, CollectionCreateModal) {
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
		}
	};
});
