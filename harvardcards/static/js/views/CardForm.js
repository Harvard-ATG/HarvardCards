define(['jquery', 'jquery.form'], function() {

    // This module sets up the card form used for adding new cards to a deck.
    // Uses the jquery.form plugin to AJAXify the html form.
    // TODO: move this to a separate JS file and modularize it.
    var CardForm = function(config) {
		if(!config || !config['formEl'] || !config['formMessageEl']) {
			throw new Error("invalid or missing CardForm config");
		}
        this.formEl = $(config.formEl);
        this.formMessageEl = $(config.formMessageEl);
    };

    CardForm.prototype.init = function() {
		var that = this;

        // set the context of the form functions to "this" instance
		// since those functions need access to properties in this object
        $.each(['beforeSubmit', 'success', 'error'], function(index, fn) {
            that.formOpts[fn] = $.proxy(that.formOpts[fn], that);
        });

        // use the jQuery.form plugin to AJAXify the form
        this.formEl.ajaxForm(this.formOpts);
    };

	// Status types for showing messages (constants)
	CardForm.STATUS_INFO = "info";
	CardForm.STATUS_SUCCESS = "success";
	CardForm.STATUS_ERROR = "error";

	// Displays a message about the status of the form.
	CardForm.prototype.message = function(html, statusType) {
		var css, status_map = {};

		status_map[CardForm.STATUS_SUCCESS] = {color:"green"};
		status_map[CardForm.STATUS_ERROR] = {color:"red"};
		status_map[CardForm.STATUS_INFO] = {color:"black"};

		css = status_map[statusType];
		if(!css) {
			css = status_map[CardForm.STATUS_INFO];
		}

		this.formMessageEl.css(css).html(html);
	};

	// Options bpassed to the jQuery.form plugin
    CardForm.prototype.formOpts = {
        resetForm: true,
        beforeSubmit: function() {
			this.message("Saving card...", CardForm.STATUS_INFO);
        },
        success: function(responseText, statusText, xhr, formEl) {
            //console.log("success", arguments);
			this.message("Card saved", CardForm.STATUS_SUCCESS);
        },
        error: function(xhr, textStatus, errorThrown) {
			this.message("Error saving card: " + textStatus, CardForm.STATUS_ERROR);
        }
    };

	return CardForm;
});
