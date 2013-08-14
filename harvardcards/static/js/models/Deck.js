define(['jquery', 'lodash', 'bootstrap', 'models/Card'], function($, _, bootstrap, Card){
	var Deck = function(collection_id, deck_id){
		this.deck_id = deck_id;
		this.collection_id = collection_id;
		this.current_card = '';
	}
	
	_.extend(Deck.prototype, {
		collectionNav: function(){
			var collection_id = this.collection_id;
			$('.collection-home-link').click(function(){
				window.location = "/index";
			});
			$('.collection-link[data-id='+collection_id+']').addClass("active-collection");
			
		},
		deckLink: function(){
			var current_deck_id = this.deck_id;
			$('.deck-link').click(function(){
				deck_id = $(this).data("id");
				if(deck_id == '')
					alert("Error: invalid deck-link");
				else
					window.location = "/deck/"+deck_id;
			});
			// activate the current
			$('.deck-link[data-id='+current_deck_id+']').addClass("active-deck");
		},
		
		newDeckButton: function(){
			$('#add-deck-button').click(function(){
				window.location = "/deck/";				
			});
		},
		// this only happens if there is no deck id associated
		initNewDeck: function(){
			var collection_id = this.collection_id;
			var deck_id = this.deck_id;
			// create an input
			if(deck_id == ''){
				// setup the input
				this.setupEditable(collection_id);
			}
			// else do nothing
		},
		setupTitle: function(){
			// click title
		},

		// make the div editable
		setupEditable: function(collection_id){
			$('.deck-title-text').editable(function(value, settings){
				return value;
			}, { 
				tooltip   : 'Click to edit...',
				cssclass: 'editable',
				style: 'inherit',
				onblur: 'submit',
				// save it when done editing...
				callback: function(value, settings){
					//var collection_id = this.collection_id;
					// send ajax to save it
					$.ajax({
						type: 'POST',
						url: '/deck/create/',
						data: {title: $(this).html(), collection_id: collection_id},
						success: function(data, statusText){
							if(data.success){
								window.location = "/deck/"+data.id;
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
			$('.deck-title-text').trigger('click');
			
		},
		
		// displays proper card
		setCurrentCard: function(card){
			this.current_card = card;
			// display card
			this.current_card.display();
		},
		
		// set the click on the cards
		initCarouselCards: function(){
			var that = this;
			$('.carousel-card').click(function(){
				$('.active-carousel-card').removeClass("active-carousel-card");
				$(this).addClass("active-carousel-card");
				var card_id = $(this).data("id");
				var card = new Card(that.collection_id, that.deck_id, card_id);
				that.setCurrentCard(card);
				// TODO: set class of clicked carousel-card

			});
		}
	
	
	});
	
	return Deck;
	
});