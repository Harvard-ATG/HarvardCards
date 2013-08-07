define(['jquery', 'lodash', 'bootstrap', 'models/Field'], function($, _, bootstrap, Field){
	var Card = function(collection_id, deck_id, card_id){
		this.collection_id = collection_id;
		this.deck_id = deck_id;
		this.card_id = card_id;
		this.field_data = '';
		this.fields = [];
	}
	
	_.extend(Card.prototype, {
		// initiate new card
		initNewCard: function(){
			collection_id = this.collection_id;
			// get the field data for the collection
			if(this.field_data){
				this.setupFieldUI();
			} else {
				this.getFieldData(collection_id);
			}
		},
		
		getFieldData: function(){
			var that = this;
			var collection_id = this.collection_id;
			$.ajax({
				type: 'POST',
				url: '/collection/fields/',
				data: {collection_id: collection_id},
				success: function(data, statusText){
					if(data.fields !== undefined){
						that.setFieldData(data.fields);
						that.initNewCard();
					} else {
						alert("Error: "+data.error)
					}
				},
				error: function(request, statusText){
					alert("Request failed.");
				}
			});
		},
		
		setFieldData: function(field_data){
			var that = this;
			this.field_data = field_data;
			this.field_data.forEach(function(field){
				f = new Field(field.label, field.field_type, field.id, field.display);
				that.fields.push(f);
			});
		},
		
		setupFieldUI: function(){
			// run through each field item
			var hide_bar = '<li class="hide-bar"> </i> ';
			var display = true;
			this.fields.forEach(function(field){
				// insert into card-main
				if(display && !field.display) {
					display = false;
					$('.card-main').append(hide_bar);
				}
				$('.card-main').append(field.template);
			});
		
		}
		
		
	});
	
	return Card;
	

});