define(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){
	var Deck = function(deck_id){
		var id = deck_id;
	}
	
	_.extend(Deck.prototype, {
		collectionNav: function(){
			$('.collection-home-link').click(function(){
				window.location = "/index";
			});
			
		},
		
		newDeckButton: function(){
			
		},
		newDeckInit: function(){
			// create an input
		},
		setupTitle: function(){
			// click title
		},
		setupEditable: function(){
			// make the div editable
			$('.deck-text').editable(function(value, settings){
				return value;
			}, { 
				tooltip   : 'Click to edit...',
				cssclass: 'editable',
				style: 'inherit',
				onblur: 'submit',
				// save it when done editing...
				callback: function(value, settings){
					// send ajax to save it
					$.ajax({
						type: 'POST',
						url: '/deck/create/',
						data: {title: $(this).html(), deck_id: $(this).data('deck_id')},
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
			
					// add data to element
			
				}
			});
		}
	
	
	});
	
	return Deck;
	
});