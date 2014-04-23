define(['jquery', 'components/InlineEditor'], function($, InlineEditor) {
	return {
		// Add confirm message to every element with a data-confirm attribute
		setupConfirm: function() {
			$("[data-confirm]").each(function(index, el) {
				var confirm_msg = $(this).data('confirm'); 
				if(confirm_msg) {
					$(this).on("click", function() {
						return window.confirm(confirm_msg);
					});
				}
			});
		},
		// Add ability to edit inline every element with data-editable=yes.
		// Note: also requires data-editable-url (API endpoint)
		// and data-editable-field (name of the field to POST to the API)
		setupEditableTitle: function() {
			$("[data-editable]").each(function(index, el) {
				var $el = $(el);
				var editable = $el.data('editable') || 'no';
				var url = $el.data('editable-url') || '';
				var field = $el.data('editable-field') || '';

				if(editable !== 'yes') {
					return;
				}

				var editor = new InlineEditor($el, {
					url: url,
					name: field,
					success: function(data, textStatus, xhr) {
						var success = data.success;
						if(!success) {
							window.alert("Error saving: "+ data.errors[field]);
						}
						return success;
					},
					error: function(xhr, textStatus, errorThrown) {
						window.alert("Error saving: "+ errorThrown);
					}
				});
			});
		}
	};
});
