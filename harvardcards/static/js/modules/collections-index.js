define(['jquery', 'components/slider/CollectionSlider'], function($, CollectionSlider) {
	return {
		initModule: function(){
			$('.slider').each(function(index, el) {
				var slider = new CollectionSlider(el);
			});
		}
	};
});
