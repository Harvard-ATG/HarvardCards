define(['jquery', 'utils/utils'], function($, utils) {
    var courseAccordion = function(courseHeader){
        var courseBody = $(courseHeader).next();
        $(courseBody).toggle('slow', function(){
            var collection_id = $(courseHeader).data('collection-id');
            if($(courseBody).is(":visible")){
                localStorage.setItem('show-collection-id'+collection_id, true);
            } else {
                localStorage.setItem('show-collection-id'+collection_id, false);
            }
        });
        $(courseHeader).find('.plusminus').toggleClass("fa-plus-circle fa-minus-circle");
        return true;
    }

    var currently = 'all open';
    var expandCollapseAll = function(){
        $('.courseHeader').each(function(index){
            var el = this;
            var body = $(el).next();
            var collection_id = $(el).data('collection-id');
            if(currently == 'all open'){
                $(body).show('slow');
                localStorage.setItem('show-collection-id'+collection_id, true);
            } else {
                $(body).hide('slow');
                localStorage.setItem('show-collection-id'+collection_id, false);
            }
        });
        if(currently == 'all open'){
            currently = 'all closed';
        } else {
            currently = 'all open';
        }

    }


    return {
		initModule: function(){
            $('.courseHeader').click(function(){ return courseAccordion(this); });
            $('#expandCollapseAllBtn').click(expandCollapseAll);

            $('.courseHeader').each(function(index){
                var el = this;
                var collection_id = $(el).data('collection-id');
                if(localStorage.getItem('show-collection-id'+collection_id) == 'true'){
                    courseAccordion(el);
                } else if(localStorage.getItem('show-collection-id'+collection_id) == undefined){
                    courseAccordion(el);
                }
            });

		}
	};
});
