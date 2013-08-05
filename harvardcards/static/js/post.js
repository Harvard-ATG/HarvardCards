(function($) {
	define([], function() {
		$.extend({
			postGo: function(url, params) {
				var csrftoken = $.cookie('csrftoken');
				var $form = $("<form>").attr("method", "post").attr("action", url);
				params['csrfmiddlewaretoken'] = csrftoken;
				$.each(params, function(name, value) {
					$("<input type='hidden'>").attr("name", name).attr("value", value).appendTo($form);
				});
				$form.appendTo("body");
				$form.submit();
			}
		});
	});
})(jQuery);