define(['jquery', 'jqueryui'], function($) {

	function sortDecks() {
		//console.log("init sort decks");

		var $sortableElement = $("#sortable-decks");

		// initialize sortable
		$sortableElement.sortable();

		// get the new order when sorting has stopped 
		$sortableElement.on("sortstop", function(event, ui) {
			//console.log("sortable event", "args:", event, ui);

			var deck_ids = []; 
			var deck_order = [];
			var deck_json = '';

			// find all deck IDs as they are ordered in the DOM
			$(event.target).find("[data-deck-id]").each(function(index, el) {
				var id = $(el).data("deck-id");
				deck_ids.push(id);
			});

			// convert to a list that explicitly has the sort order 
			deck_order = $.map(deck_ids, function(val, index) {
				var sort_order = index + 1; // because index starts at zero
				return {"sort_order": sort_order, "deck_id": val};
			});

			// convert to JSON format so it can be stored in a hidden input field
			// that will be POSTed along with the rest of the form
			deck_json = JSON.stringify({"deck": deck_order});

			$("#deck_order").val(deck_json).effect("highlight");

			//console.log("--> new deck order:", deck_ids, deck_order);
		});
	}

	var MODULE = {
		initModule: function(el) {
			sortDecks();
		}
	};

	return MODULE;
});
