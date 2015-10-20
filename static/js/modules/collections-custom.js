define(['jquery', 'jqueryui', 'utils/utils'], function($, $ui, utils) {
	return {
		initModule: function(el) {
			var $form = $("#customForm");
			utils.setupMaskOnFormSubmit($form);
		}
	};
});

