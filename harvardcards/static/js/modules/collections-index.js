define(['jquery', 'components/slider/CollectionSlider', 'utils/utils', 'jqueryui'], function($, CollectionSlider, utils) {
	return {
		initModule: function(){


            $('.courseHeader').click(function() {
                var el = this;
                $(this).next().toggle('slow', function(){
                    var collection_id = $(el).data('collection-id');
                    if($(el).next().is(":visible")){
                        localStorage.setItem('show-collection-id'+collection_id, true);
                    } else {
                        localStorage.removeItem('show-collection-id'+collection_id);
                    }
                });
                $(this).find('.plusminus').toggleClass("fa-plus-circle fa-minus-circle");
                return false;
            }).next().hide();

            $('.courseHeader').each(function(index){
                var el = this;
                var collection_id = $(el).data('collection-id');
                if(localStorage.getItem('show-collection-id'+collection_id) == 'true'){
                    $(el).click();
                }
            });

		}
	};
});
