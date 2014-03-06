define(['jquery', 'views/CardTemplatePreview'], function($, CardTemplatePreview) {
	return {
		initModule: function(el) {
			var preview = new CardTemplatePreview({
				"previewEl": "#cardTemplateContainer",
				"selectEl": "#id_card_template"
			});
			preview.init();
		}
	};
});
