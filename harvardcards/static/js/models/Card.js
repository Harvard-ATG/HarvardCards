define(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){
	var Card = function(collection_id, deck_id, card_id){
		this.collection_id = collection_id;
		this.deck_id = deck_id;
		this.card_id = card_id;
	}
	
	_.extend(Card.prototype, {
		
		// initiate new card
		initNewCard: function(){
			collection_id = this.collection_id;
			// get the field data for the collection
			this.getFieldData(collection_id);
		},
		
		getFieldData: function(){
			var collection_id = this.collection_id;
			$.ajax({
				type: 'POST',
				url: '/collection/fields/',
				data: {collection_id: collection_id},
				success: function(data, statusText){
					if(data.success){

					} else {
						alert("Error: "+data.message)
					}
				},
				error: function(request, statusText){
					alert("Request failed.");
				}
			});
		}
		
		
	});
	
	return Card;
	

});