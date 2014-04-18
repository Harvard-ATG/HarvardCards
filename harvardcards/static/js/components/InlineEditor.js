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
			select: true
		};

		this.url = this.options.url || '';
		this.name = this.options.name || 'field_name';
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
		var data = {};
		data[editor.name] = value;

		var deferred = $.ajax({
			url: editor.url,
			method: 'POST',
			dataType: 'json',
			data: data
		});
		
		deferred.done(editor.onSuccess);
		deferred.fail(editor.onError);

		return value;
	};

	InlineEditor.prototype.onSuccess = function(data, textStatus, xhr) {
		this.highlight({color: "yellow"});
		this.success.apply(this, arguments); 
	};

	InlineEditor.prototype.onError = function(xhr, textStatus, errorThrown) {
		this.highlight({color: "red"});
		this.error.apply(this, arguments);
	};

	InlineEditor.prototype.highlight = function(options) {
		$(this.el).effect("highlight", options, 1500);
	};

	return InlineEditor;
});
