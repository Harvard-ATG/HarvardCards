define(['jquery', 'utils/utils'], function($, utils) {
	var courseAccordion = function(courseHeader){
        var courseBody = $(courseHeader).next();
        $(courseBody).toggle('slow', function(){
            var collection_id = $(courseHeader).data('collection-id');
            if($(courseBody).is(":visible")){
                localStorage.setItem('show-collection-id'+collection_id, true);
            } else {
                localStorage.removeItem('show-collection-id'+collection_id);
            }
        });
        $(courseHeader).find('.plusminus').toggleClass("fa-plus-circle fa-minus-circle");
        return true;
    }

    return {
		initModule: function(){
            $('.courseHeader').click(function(){ return courseAccordion(this); });

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
