define(['jquery', 'jqueryui'], function($, $ui) {

    var CollectionCreateModal = function(options) {
        this.options = options;
        this.btnSelector = this.options.btnSelector;
        this.dialogSelector = this.options.dialogSelector;
    };

    $.extend(CollectionCreateModal.prototype, {
        init: function() {
            this.modalHandler = $.proxy(this.modalHandler, this);

            $(this.btnSelector).click(this.modalHandler);
        },
        modalHandler: function(evt) {
            $(this.dialogSelector).dialog({
                modal: true,
                width: '60%',
                title: 'Add Collection',
                position: { my: "top", at: "top+20px", of: window },
                closeOnEscape: true,
                buttons: {
                    Cancel: function() {
                        $(this).dialog("close");
                    }
                },
                open: function(event, ui) {
                    //console.log("event: open", event, ui);
                }
            });
            return false;
        }
    });

    return CollectionCreateModal;
});
