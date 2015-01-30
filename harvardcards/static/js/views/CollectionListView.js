define(['jquery'], function($) {

    var CollectionListView = function(options) {
        this.options = options;
        this.headerSelector = this.options.headerSelector;
        this.btnSelector = this.options.btnSelector;
        console.log(this);
    };

    $.extend(CollectionListView.prototype, {
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
            return $(this.headerSelector);
        },
        getExpandCollapseAllBtn: function() {
            return $(this.btnSelector);
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
    });

    return CollectionListView;
});