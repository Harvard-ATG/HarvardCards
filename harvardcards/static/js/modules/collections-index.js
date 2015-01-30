define([
'jquery',
'jqueryui',
'views/CollectionListView'
],
function(
$,
$ui,
CollectionListView) {

    var CollectionCreateModal = {
        init: function() {
            console.log("init modal");
            this.modalHandler = $.proxy(this.modalHandler, this);
            $("#addAcourse").click(this.modalHandler);
        },
        modalHandler: function(evt) {
            console.log("click", this, arguments);
            $("#addAcourseDialog").dialog({
                modal: true,
                width: '60%',
                position: { my: "top", at: "top+20px", of: window },
                closeOnEscape: true,
                buttons: {
                    Cancel: function() {
                        $(this).dialog("close");
                    }
                },
                open: function(event, ui) {
                    console.log("event: open", event, ui);
                }
            });
            return false;
        }
    };

    return {
		initModule: function(){
		    var collection_list_view = new CollectionListView({
		        headerSelector: ".courseHeader",
		        btnSelector: "#expandCollapseAllBtn"
		    });

			collection_list_view.init();
		    CollectionCreateModal.init();
		}
	};
});
