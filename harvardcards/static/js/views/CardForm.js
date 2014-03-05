define(['jquery', 'jquery.form'], function() {

    // This module sets up the card form used for adding new cards to a deck.
    // Uses the jquery.form plugin to AJAXify the html form.
    // TODO: move this to a separate JS file and modularize it.
    var CardForm = function(config) {
        this.formEl = $(config.formEl);
        this.formMessageEl = $(config.formMessageEl);
    };

    CardForm.prototype.init = function() {
        // set the context of the form functions to "this" instance
		// since those functions need access to properties in this object
        $.each(['beforeSubmit', 'success', 'error'], $.proxy(function(index, fn) {
            this.formOpts[fn] = $.proxy(this.formOpts[fn], this);
        }, this));

        // use the jQuery.form plugin to AJAXify the form
        this.formEl.ajaxForm(this.formOpts);
    };

	// Options bpassed to the jQuery.form plugin
    CardForm.prototype.formOpts = {
        resetForm: true,
        beforeSubmit: function() {
            this.formMessageEl.css("color", "black").html('Saving card...');
        },
        success: function(responseText, statusText, xhr, formEl) {
            //console.log("success", arguments);
            this.formMessageEl.css("color", "green").html("<b>Card saved</b>");
        },
        error: function() {
            this.formMessageEl.css("color", "red").html("<b>Error: card not saved</b>");
        }
    };

	return CardForm;
});
