define(['jquery', 'microevent', 'components/slider/Slider'], function($, MicroEvent, Slider) {

	var DeckSlider = function(el, startIndex) {
		this.el = $(el);
		this.card_ids = [];
		this.currentCardId = null;
		this.currentCardEl = null;
		this.startIndex = startIndex || 0;
		this.onClickCard = $.proxy(this.onClickCard, this);

		this.init();
	};

	DeckSlider.prototype.init = function() {
		this.card_ids = this.findCardIds();

		this.slider = new Slider({
			el: this.el,
			startIndex: this.startIndex,
			plugins: {
				responsive: {
					maxShowItems: 4
				},
				keyboard: {}
			}
		});

		this.initListeners();

		if(this.card_ids[0]) {
			this.goToCard(this.card_ids[0]);
		}
	};

	// Delegate methods to Slider instance
	$.each(['goToNext', 'goToPrev', 'goToFirst', 'goToLast', 'goToCurrent'], function(index, method) {
		DeckSlider.prototype[method] = function() {
			var result = this.slider[method].apply(this.slider, arguments);
			this.selectCard(this.card_ids[this.slider.getCurrentIndex()]);
			return result;
		};
	})

	DeckSlider.prototype.initListeners = function() {
		var self = this;

		this.el.on("click", ".card", this.onClickCard);

		this.slider.bind("beforeslide", function() {
			var card_id = self.card_ids[self.slider.getCurrentIndex()];
			self.selectCard(card_id);
			self.trigger("beforeslide", self, card_id);
		});

		this.slider.bind("slide", function() {
			var card_id = self.card_ids[self.slider.getCurrentIndex()];
			self.selectCard(card_id);
			self.trigger("slide", self, card_id);
		});
	};

	DeckSlider.prototype.onClickCard = function(e) {
		var card_id, currentTarget = e.currentTarget;
		if(this.isCard(currentTarget)) {
			card_id = this.getCardId(currentTarget);
			this.goToCard(card_id);
		}
	};

	DeckSlider.prototype.findByCardId = function(card_id) {
		return $(".card[data-card-id="+card_id+"]");
	};

	DeckSlider.prototype.findCardIds = function() {
		var self = this, cards = [];
		$(this.el).find(".card").each(function(index, el) {
			cards.push(self.getCardId(el));
		});
		return cards;
	};

	DeckSlider.prototype.getCardId = function(el) {
		return $(el).data("card-id");
	};

	DeckSlider.prototype.getCurrentCardId = function() {
		return this.currentCardId;
	};

	DeckSlider.prototype.getCurrentCardNum = function() {
		return this.slider.getCurrentIndex() + 1;
	};

	DeckSlider.prototype.isCard = function(el) {
		return $(el).is("a.card");
	};

	DeckSlider.prototype.selectCard = function(card_id) {
		this.unhighlight();
		this.setCurrentCard(card_id);
		this.highlight();
	};

	DeckSlider.prototype.goToCard = function(card_id) {
		var card_index = this.card_ids.indexOf(card_id);
		if(card_index !== -1) {
			this.slider.goTo(card_index);
		}
	};

	DeckSlider.prototype.setCurrentCard = function(card_id) {
		this.currentCardEl = this.findByCardId(card_id);
		this.currentCardId = card_id;
	};

	DeckSlider.prototype.getNumItems = function() {
		return this.slider.getNumItems();
	};

	DeckSlider.prototype.unhighlight = function() {
		if(this.currentCardEl) {
			this.currentCardEl.parent().removeClass("clicked");
		}
	};

	DeckSlider.prototype.highlight = function(card_id) {
		if(this.currentCardEl) {
			this.currentCardEl.parent().addClass("clicked");
		}
	};

	DeckSlider.prototype.shuffle = function() {
		var cards  = $(this.el).find("ul#cards");
		var child = cards.children();
		var random_index;

		while (child.length) {
			random_index = Math.floor(Math.random() *  child.length);
			this.card_ids.push(this.card_ids.splice(random_index, 1)[0]);
			cards.append(child.splice(random_index, 1));
		}
	};

	MicroEvent.mixin(DeckSlider);

    return DeckSlider;
});
