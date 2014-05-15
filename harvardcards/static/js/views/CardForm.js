define(['lodash', 'jquery', 'jquery.form'], function(_, $, $form) {

    // This module sets up the card form used for adding new cards to a deck.
    // Uses the jquery.form plugin to AJAXify the html form.
    var CardForm = function(config) {
        if(!config || !config['formEl'] || !config['formMessageEl']) {
			console.log("card form", config);
            throw new Error("invalid or missing CardForm config");
        }
        this.formEl = $(config.formEl);
        this.formMessageEl = $(config.formMessageEl);
		this.error = $.proxy(this.error, this);
		this.success = $.proxy(this.success, this);
    };

    CardForm.prototype.init = function() {
        // bind these methods to the "this" context since they
        // will be passed to the jQuery form plugin
        _.bindAll(this, ['beforeSubmit', 'success', 'error']);

        // use the jQuery.form plugin to AJAXify the form
        this.formEl.ajaxForm({
            resetForm: false,
            beforeSubmit: this.beforeSubmit,
            error: this.error,
            success: this.success
        });
	};

    // Status types for showing messages (constants)
    var MSG_INFO = CardForm.MSG_INFO = "info";
    var MSG_SUCCESS = CardForm.MSG_SUCCESS = "success";
    var MSG_ERROR = CardForm.MSG_ERROR = "error";

    CardForm.prototype.beforeSubmit = function() {
        this.msg("Saving card...", MSG_INFO);
    };

    CardForm.prototype.success = function(data, statusText, xhr, formEl) {
        console.log("success", arguments);
        if (data.success){
            this.msg("Card saved", MSG_SUCCESS);
            window.setTimeout(this.makeRedirect(data.location), 500)
        } else {
            var errors = '';
            $.each(data.error, function(index, errstr) {
                errors += '<li>' + errstr + '</li>';
            });
            errors = '<ul>' + errors + '</ul>';
            this.msg(errors, MSG_ERROR);
        }
    };

    CardForm.prototype.makeRedirect = function(location) {
        return function() {
            window.location = location;
        };
    };

    CardForm.prototype.error = function(xhr, textStatus, errorThrown) {
        this.msg("Card error: " + textStatus, MSG_ERROR);
    };

    // Displays a message about the status of the form.
    CardForm.prototype.msg = function(html, statusType) {
        this.formMessageEl.css('display', 'block');
        var css, css_for = {};
        css_for[MSG_SUCCESS] = {color:"green"};
        css_for[MSG_ERROR] = {color:"red"};
        css_for[MSG_INFO] = {color:"black"};

        css = css_for[statusType];
        if(!css) {
            css = css_for[MSG_INFO];
        }
        this.formMessageEl.css(css).html(html);
    };

    return CardForm;
});
