define(['jquery', 'jquery.jeditable', 'jqueryui'], function($) {

	/**
	 * Wrapper object for creating an inline editor.
	 * Delegates to the jquery.jeditable object.
	 */
	var InlineEditor = function(el, options) {
		this.el = $(el);
		this.options = options || {};
		this.onSuccess = $.proxy(this.onSuccess, this);
		this.onError = $.proxy(this.onError, this);
		this.init();
	};

	InlineEditor.prototype.init = function() {
		var that = this;
		var editorConfig = {
			select: true,
			submit: "Save",
			cancel: "Cancel"
		};

		this.edit = this.options.edit || function() {}; // edit callback
		this.success = this.options.success || function() {}; // success callback
		this.error = this.options.error || function() {}; // error callback

		this.el.editable(this.makeTargetHandler(), editorConfig);
	};

	InlineEditor.prototype.makeTargetHandler = function() {
		var that = this;
		return function() {
			var args = Array.prototype.slice.call(arguments);
			args.unshift(that);
			return that.handleEdit.apply(this, args);
		};
	};

	InlineEditor.prototype.handleEdit = function(editor, value, settings) {
		var deferred = editor.edit(editor, value, settings);
		deferred.done(editor.onSuccess);
		deferred.fail(editor.onError);
		return value;
	};

	InlineEditor.prototype.onSuccess = function(data, textStatus, xhr) {
		return this.success.apply(this, arguments);
	};

	InlineEditor.prototype.onError = function(xhr, textStatus, errorThrown) {
		this.error.apply(this, arguments);
	};

	InlineEditor.prototype.highlight = function(options) {
		$(this.el).effect("highlight", options, 1500);
	};

	return InlineEditor;
});
