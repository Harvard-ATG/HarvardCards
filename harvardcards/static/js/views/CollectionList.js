define(['jquery', 'lodash'], function($, _){

	var CollectionList = function(config){
		this.config = config;

		this.init();
	};
	
	_.extend(CollectionList.prototype, {
		init: function(){
			this.initCreateButton();
		},
		
		initCreateButton: function(){
			var that = this;
			that.config.add_collection_button.click(function(){
				// show the collection
				that.config.add_collection_content.show();
				

			});
		},
		
		
	});
	
	return CollectionList;	
	
	
});