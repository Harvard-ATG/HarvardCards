define(['./API'], function(API) {

	var Deck = function(config) {
		config = config || {};
		this.id = config.id || null;
		this.title = config.title || '';
	};

	Deck.prototype.rename = function(title) {
		this.title = title;
		var deferred = API.ajax('deck/rename', {
			method: 'POST',
			data: {
				deck_id: this.id,
				title: this.title
			}
		});
		return deferred;
	};

	return Deck;
});
