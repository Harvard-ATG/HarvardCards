define(['jquery', 'lodash', 'models/Collection'], function($, _, Collection){

	var CollectionList = function(config){
		this.config = config;
		this.newCollection = {};
		// these are required
		// TODO: checkConfig method
		//$add_collection_button
		//$add_collection_content
		//$add_collection_title
		this.init();
	};
	
	_.extend(CollectionList.prototype, {
		init: function(){
			this.initNewCollection();
			this.initCreateButton();
			this.initTitleEditable();
		},
		
		initNewCollection: function(){
			var that = this;
			// create a new collection object
			that.newCollection = new Collection();
		},
		
		initCreateButton: function(){
			var that = this;
			that.config.$add_collection_button.click(function(){
				// show the collection
				that.config.$add_collection_content.show();
			});
		},
		
		initTitleEditable: function(){
			var that = this;
			that.config.$add_collection_title.editable(function(value, settings){
				return value;
			}, { 
				tooltip   : 'Click to edit...',
				style: 'inherit',
				onblur: 'submit',
				callback: function(value, settings){
					that.newCollection.title = value;
				}
			});
		},
		
		
	});
	
	return CollectionList;	
	
	
});