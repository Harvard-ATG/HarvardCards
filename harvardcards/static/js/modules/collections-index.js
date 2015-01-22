define(['jquery', 'components/slider/CollectionSlider', 'utils/utils', 'jqueryui'], function($, CollectionSlider, utils) {
	return {
		initModule: function(){
            $('.courseHeader').click(function() {
                $(this).next().toggle('slow');
                $(this).find('.plusminus').toggleClass("fa-plus-circle fa-minus-circle");
                return false;
            }).next().hide();

		}
	};
});
