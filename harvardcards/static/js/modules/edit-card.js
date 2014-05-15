define(['jquery', 'views/CardForm'], function($, CardForm) {
	return {
		initModule: function(el) {
			var cardform = new CardForm({
				"formEl": "#cardForm",
				"formMessageEl": "#cardForm .formMessage"
			});
			cardform.init();
		}
	};
});
