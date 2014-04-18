define(['jquery', 'components/slider/CollectionSlider', 'utils/utils'], function($, CollectionSlider, utils) {
	return {
		initModule: function(){
			$('.slider').each(function(index, el) {
				var slider = new CollectionSlider(el);
			});

			utils.setupConfirm();
		}
	};
});
