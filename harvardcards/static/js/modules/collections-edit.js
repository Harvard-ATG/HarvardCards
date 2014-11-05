define(['jquery', 'jqueryui'], function($) {

	function sortDecks() {
		console.log("init sort decks");

		var $sortableElement = $("#sortable-decks");

		// initialize sortable
		$sortableElement.sortable();

		// get the new order when sorting has stopped 
		$sortableElement.on("sortstop", function(event, ui) {
			console.log("sortable event", "args:", event, ui);

			var deck_ids = []; 
			var json_deck_ids = '';

			$(event.target).find("[data-deck-id]").each(function(index, el) {
				var id = $(el).data("deck-id");
				deck_ids.push(id);
			});

			json_deck_ids = JSON.stringify({"deck_ids": deck_ids});
			$("#deck_order").val(json_deck_ids);

			console.log("new deck order: ", deck_ids, "json:", json_deck_ids);
		});
	}

	var MODULE = {
		initModule: function(el) {
			console.log("init collecitons edit");
			sortDecks();
		}
	};

	return MODULE;
});
