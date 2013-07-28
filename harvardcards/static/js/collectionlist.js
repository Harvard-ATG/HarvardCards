require(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){

	var CollectionList = function(){
		this.init();
	};
	
	_.extend(CollectionList.prototype, {
		init: function(){
			this.addButton();
			this.deleteButton();
			this.editButton();
			this.activate();
		},
		
		addButton: function(){
			$('#add_collection_button').click(function(){
				window.location = "/collection/create";
			});
		},
		
		deleteButton: function(){
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
		},
		
		editButton: function(){
			$('#edit_collection_button').click(function(){
				collection_id = $('.active-collection').parent().data("id");
				window.location = "/collection/create/" + collection_id;
			});			
		},
		
		activate: function(){
			$('.collection-list-item a').click(function(){
				$('.active-collection').removeClass("active-collection");
				// setting it on the a because of the bgcolor, on the parent doesn't fill the element
				$(this).addClass("active-collection");
			});
		}
		
	});
	
	return new CollectionList();	
	
	
});