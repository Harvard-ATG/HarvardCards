define(['jquery', 'jqueryui', 'utils/utils'], function($, $ui, utils) {
	return {
		initModule: function(el) {
			var $form = $("#deckForm");
			utils.setupMaskOnFormSubmit($form);
		}
	};
});

