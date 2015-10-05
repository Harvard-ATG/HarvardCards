define(['jquery'], function($) {
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
		setupMaskOnFormSubmit: function($form) {
			$form.on('submit', function(evt) {
				$("#bodymask").show();
			});
		}
	};
});
