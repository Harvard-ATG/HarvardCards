define(['jquery'], function($) {
	return {
		setupConfirm: function() {
			$("[data-confirm]").each(function(index, el) {
				var confirm_msg = $(this).data('confirm'); 
				if(confirm_msg) {
					$(this).on("click", function() {
						return window.confirm(confirm_msg);
					});
				}
			});
		}
	};
});
