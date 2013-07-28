require(['jquery', 'bootstrap'], function($, bootstrap){

	$('#add_collection_button').click(function(){
		window.location = "/collection/create";
	});
	$('#delete_collection_confirm_button').click(function(){
		if($('.active-collection').length){
			$('#collectionDeleteModal').modal();
			
		}
	});
	$('#delete_collection_button').click(function(){
		collection_id = $('.active-collection').parent().data("id");
		// send to the delete
		$.ajax({
			url: '/collection/delete',
			data: {id: collection_id},
			success: function(data, statusText){
				if(data.success){
					$('#collectionDeleteModal').modal('hide');
					// remove item from UI
					$('.active-collection').parent().remove();
					$('#course-' + collection_id).remove();
					// if it's the last one removed, make sure the no-collections-items are shown
					if($('.collection-list-item').length == 0)
						$('.no-collections-item').removeClass("hide");
				} else {
					alert("Error deleting.")
				}
			},
			error: function(request, statusText){
				alert("Request failed.");
			}
		});
	});
	$('#edit_collection_button').click(function(){
		collection_id = $('.active-collection').parent().data("id");
		window.location = "/collection/create/" + collection_id;
	});
	$('.collection-list-item a').click(function(){
		$('.active-collection').removeClass("active-collection");
		// setting it on the a because of the bgcolor
		$(this).addClass("active-collection");
	});
	
	deckCount = 0;
	$('.new-deck-btn').click(function(){
		// new temporary ID for the element
		tempId = 'tmpdeck'+deckCount;
		// create a new <li> there
		var deckTmpl = '<li class="deck"><div id="'+tempId+'" class="deck-text">Deck Name</div></li>';
		$(this).parent().append(deckTmpl);
		var collection_id = $(this).data('collection_id');
		//console.log("collection_id: "+ collection_id);
		// add the editable field
		$('#'+tempId).editable(function(value, settings){
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
					data: {title: $('#'+tempId).html(), collection_id: collection_id},
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
		// activate it
		$('#'+tempId).trigger('click');
				
		deckCount++;
	});
	
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
	$('.deck').mouseover(function(){
		$(this).children('.deck-controls').removeClass('hide');
		$(this).children('.deck-delete-btn').removeClass('hide');
		
	});
	$('.deck').mouseout(function(){
		$(this).children('.deck-controls').addClass('hide');
		$(this).children('.deck-delete-btn').addClass('hide');
		
	});
	
	$('.deck-delete-btn').click(function(){
		listItem = $(this).parent();
		$.ajax({
			type: 'POST',
			url: '/deck/delete/',
			data: {deck_id: listItem.data('deck_id')},
			success: function(data, statusText){
				if(data.success){
					listItem.remove();
				} else {
					alert("Error: "+data.message)
				}
			},
			error: function(request, statusText){
				alert("Request failed.");
			}
		});
	});
	
	
	
});