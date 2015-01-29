define(['jquery', 'utils/utils', 'jqueryui'], function($, utils) {

    var CollectionListView = {
        init: function() {
            var self = this;

            this.allCollapsed = true;

            this.getHeaderEls().click(function() {
                self.toggleCollapse(this);
            });

            this.getExpandCollapseAllBtn().click(function() {
                var el = this;
                self.toggleCollapse(self.getHeaderEls(), self.allCollapsed);
                self.allCollapsed = !self.allCollapsed;
                $(el).find('span').html(self.allCollapsed?'Expand All':'Collapse All');
                self.togglePlusMinusCls(el);
            });

            this.getHeaderEls().each(function(index, el) {
                var collection_id = $(el).data('collection-id');
                var collection_state = localStorage.getItem('show-collection-id'+collection_id);

                if(collection_state == 'true'){
                    self.toggleCollapse(el, true);
                } else if(collection_state == undefined){
                    self.toggleCollapse(el, false);
                }
            });
        },
        getHeaderEls: function() {
            return $('.courseHeader');
        },
        getExpandCollapseAllBtn: function() {
            return $('#expandCollapseAllBtn');
        },
        toggleCollapse: function(headerEls, state) {
            var self = this;
            $(headerEls).each(function(index, el) {
                var courseBody = $(el).next();
                var visible = $(courseBody).is(":visible");
                if(typeof state === 'undefined' || state != visible) {
                    $(courseBody).slideToggle('slow', function(){
                        var collection_id = $(el).data('collection-id');
                        var visible = $(courseBody).is(":visible");
                        localStorage.setItem('show-collection-id'+collection_id, visible);
                    });
                    self.togglePlusMinusCls(el);
                }
            });
        },
        togglePlusMinusCls: function(el) {
            $(el).find('.plusminus').toggleClass('fa-plus-circle fa-minus-circle');
        }
    };

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
                width: '95%',
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
		    CollectionListView.init();
		    CollectionCreateModal.init();
		}
	};
});
