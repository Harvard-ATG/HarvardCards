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
			this.config.add_collection_button.click(function(){
				

			});
		},
		
		
	});
	
	return CollectionList;	
	
	
});