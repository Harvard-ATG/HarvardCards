define('models/Card', ['jquery', 'lodash', 'models/Field'], function($, _, Field){
	var Card = function(collection_id, deck, card_id){
		this.collection_id = collection_id;
		this.deck_id = deck.deck_id;
		this.card_id = card_id;
		this.field_data = '';
		this.fields = [];
		//console.log(Field);
		this.deck = deck;
	}
	
	_.extend(Card.prototype, {
		// initiate new card
		initNewCard: function(){
			collection_id = this.collection_id;
			// get the field data for the collection
			if(this.field_data){
				this.setupFieldUI();
				this.saveCardButton();
			} else {
				this.getFieldData('new');
			}
		},
		
		getFieldData: function(type){
			var that = this;
			var collection_id = this.collection_id;
			$.ajax({
				type: 'POST',
				url: '/collection/fields/',
				data: {collection_id: collection_id},
				success: function(data, statusText){
					if(data.fields !== undefined){
						that.setFieldData(data.fields);
						if(type == 'new'){
							that.initNewCard();
						} else {
							that.display();
						}
					} else {
						alert("Error: "+data.error)
					}
				},
				error: function(request, statusText){
					alert("Request failed.");
				}
			});
		},
		
		getFieldValues: function(mycallback, mycallbackObj){
			var that = this;
			$.ajax({
				type: 'POST',
				url: '/card/fields/',
				data: {card_id: that.card_id},
				success: function(data, statusText){
					if(data.fields !== undefined){
						data.fields.forEach(function(field){
							f = new Field(field.label, field.field_type, field.field_id, field.display, field.value, field.cards_fields_id);
							that.fields.push(f);
						});
						mycallback.apply(mycallbackObj);
					} else {
						alert("Error: "+data.error);
					}
					
					//mycallback();
				},
				error: function(request, statusText){
					alert("request failed.");
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
			this.clearCardView();
			// run through each field item
			var hide_bar = '<li class="hide-bar"> </i> ';
			var display = true;
			this.fields.forEach(function(field){
				// insert into card-main
				if(display && !field.display) {
					display = false;
					$('.card-main').append(hide_bar);
				}
				if(field.value !== undefined){
					$('.card-main').append(field.view_template);
				} else {
					$('.card-main').append(field.edit_template);
				}
			});
			// save button or delete button
			if(this.card_id !== undefined){
				$('.card-main-save').addClass("hide");
				$('.card-main-delete').removeClass("hide");
				// set the id for the delete button
				$('.delete-card-btn').data("id", this.card_id);
				this.deleteCardButton();
				this.setFieldEditables();
			} else {
				$('.card-main-save').removeClass("hide");
				$('.card-main-delete').addClass("hide");				
			}
		
		},
		saveCardButton: function(){
			var that = this;
			$('.save-card-btn').unbind("click");
			$('.save-card-btn').click(function(){
				card_id = '';
				// collect data
				var fields = [];
				$('.field-template input').each(function(keys, input){
					var field = {};
					field['value'] = $(input).val();
					field['field_id'] = $(input).data("id");
					fields.push(field);
				});
				// json stringify the fields object
				json_fields = JSON.stringify(fields);
				// send data to the server
				$.ajax({
					type: 'POST',
					url: '/card/create/',
					data: {fields: json_fields, card_id: card_id, collection_id: that.collection_id, deck_id: that.deck_id},
					success: function(data, statusText){
						if(data.card_data !== undefined){
							console.log(data);
							// TODO: add card to carousel
							//alert("success! TODO: add card to carousel");
							new_carousel_card = $('.carousel-card-template').clone();
							new_carousel_card.removeClass("carousel-card-template");
							new_carousel_card.css("display", "inline-block");
							new_carousel_card.html(fields[0]['value']);
							new_carousel_card.data("id", data.card_data.card_id)
							$('.card-carousel-list').append(new_carousel_card);
							that.deck.initCarouselCards();
							new_carousel_card.trigger("click");
							
						} else {
							alert("Error: no card data returned!\n")
							console.log(data);
						}
					},
					error: function(request, statusText){
						alert("Request failed!");
					}
				});
			
			});
		},
		deleteCardButton: function(){
			var that = this;
			$('.delete-card-btn').unbind("click");
			$('.delete-card-btn').click(function(){
				var card_id = $(this).data("id");
				$.ajax({
					type: 'POST',
					url: '/card/delete/',
					data: {card_id: card_id},
					success: function(data, statusText){
						// find current carousel-card
						active_carousel_card = $('.active-carousel-card');
						// click on next carousel card
						if(active_carousel_card.next().length > 0)
							active_carousel_card.next().trigger("click");
						else
							active_carousel_card.prev().trigger("click");
						// remove old carousel-card from dom
						active_carousel_card.remove();

					},
					error: function(request, statusText){
						alert("Request failed!");
					}
				})
			});
		},
		
		// this needs to set up the first card if there are no other cards
		initFirstCard: function(){
			
		},
		
		clearCardView: function(){
			$('.card-main').children().remove();
		},
		
		display: function(){
			var that = this;
			collection_id = this.collection_id;
			
			
			
			// get the field data for the collection
			if(this.field_data){
				this.setupFieldUI();
				this.saveCardButton();
			} else {
				if(this.card_id == '' || this.card_id === undefined){
					this.getFieldData();
				} else {
					//this.getFieldData();
					// doing this with a callback causes setupFieldUI to be called from the global scope! (without 'that')
					this.getFieldValues(that.setupFieldUI, that);
				}
			
			}
		},
		
		setFieldEditables: function(){
			var that = this;
			$('.text-field-template').editable(function(value, settings){
				return value;
			}, { 
				tooltip   : 'Click to edit...',
				cssclass: 'editable',
				style: 'inherit',
				onblur: 'submit',
				callback: function(value, settings){
					var cf_id = $(this).data("cf_id");
					$.ajax({
						type: 'POST',
						url: '/card/fieldEdit/',
						data: {cards_fields_id: cf_id, value: value},
						success: function(data, statusText){
							if(data.error === undefined){
								alert("success");
							} else {
								alert("error: "+data.error);
							}
						},
						error: function(request, statusText){
							alert("request failed.");
							console.log(request);
						}
					});
					
				}
			});

		}
		

		
		
	});
	
	return Card;
	

});