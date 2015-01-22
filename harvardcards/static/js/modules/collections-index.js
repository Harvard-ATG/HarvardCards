define(['jquery', 'components/slider/CollectionSlider', 'utils/utils', 'jqueryui'], function($, CollectionSlider, utils) {
	return {
		initModule: function(){
            $('.courseHeader').click(function() {
                $(this).next().toggle('slow');
                return false;
            }).next().hide();

		}
	};
});
