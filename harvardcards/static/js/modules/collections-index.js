define(['jquery', 'components/slider/CollectionSlider', 'components/ActionButton'], function($, CollectionSlider, ActionButton) {
	return {
		initModule: function(){
			$('.slider').each(function(index, el) {
				var slider = new CollectionSlider(el);
			});

			$(".js-delete-collection").each(function(index, el) {
				var delete_collection_button = new ActionButton(el, {
					before: function() {
						return window.confirm("Delete collection permanently?");
					},
					after: function(success, data) {
						if(success) {
							window.location = data.location;
						} else {
							window.alert("Error deleting collection: " + data);
						}
					}
				});
			});
		}
	};
});
