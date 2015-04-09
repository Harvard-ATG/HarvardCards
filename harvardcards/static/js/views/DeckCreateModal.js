define(['jquery', 'jqueryui'], function($, $ui) {

    var DeckCreateModal = function(options) {
        this.options = options;
        this.btnSelector = this.options.btnSelector;
        this.dialogSelector = this.options.dialogSelector;
        this.form_name = this.options.form_name;
    };

    $.extend(DeckCreateModal.prototype, {
        init: function() {
            this.modalHandler = $.proxy(this.modalHandler, this);

            $(this.btnSelector).click(this.modalHandler);
        },
        modalHandler: function(evt) {
            $(this.dialogSelector).dialog({
                modal: true,
                width: '60%',
                position: { my: "top", at: "top+20px", of: window },
                closeOnEscape: true,
                buttons:[{
                            click: $.noop,
                            text: "Submit",
                            type: "Submit",
                            form: this.form_name
                        },
                        {
                            click: function() {
                                    $(this).dialog("close");
                                },
                            text: "Close"
                        }],
                open: function(event, ui) {
                    $( this ).find( "[type=submit]" ).hide();
                    //console.log("event: open", event, ui);
                }
            });
            return false;
        }
    });

    return DeckCreateModal;
});