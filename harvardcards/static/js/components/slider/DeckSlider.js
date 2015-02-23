define(['jquery', 'microevent', 'components/slider/Slider'], function($, MicroEvent, Slider) {

	/**
	 * The DeckSlider is responsible for displaying a list of 
	 * cards as a slider. 
	 *
	 * The slider may be controlled by the buttons on the screen
	 * to advance to the next/previous or first/last cards, by
	 * clicking on cards displayed on screen, or by using the keyboard.
	 *
	 * On mobile screen sizes, the slider will be hidden and a different
	 * set of buttons placed at the bottom of the screen will be displayed
	 * to control the slider.
	 *
	 * The slider knows how to "play" and "shuffle" the cards.
	 *
	 * Events (see MicroEvent):
	 *		- beforeslide : triggered before the slide
	 *		- slide       : triggered after the slide
	 *
	 * Usage:
	 *		var slider = new CollectionSlider($("#slider"));
	 *		slider.goToNext();
	 *		slider.goToPrev();
	 */
	var DeckSlider = function(el) {
		this.el = $(el);

		this.card_ids = [];
		this.currentCardId = this.el.data('start-card-id');
		this.currentCardIndex = 0;
		this.currentCardEl = null;
		this.playbackDelay = 4000;
		this._playIntervalId = null;

		// bind methods to the "this" context
		this.onClickCard = $.proxy(this.onClickCard, this);
		this.onBeforeSlide = $.proxy(this.onBeforeSlide, this);
		this.onSlide = $.proxy(this.onSlide, this);

		this.init();
	};

	// Initializes the slider.
	DeckSlider.prototype.init = function() {
		this.card_ids = this.findCardIds();
		this.loaded = {};
		this.loadSize = 4;

		if(this.currentCardId) {
			this.setCurrentCard(this.currentCardId);
		} else if(this.card_ids.length > 0) {
			this.setCurrentCard(this.card_ids[0])
		}

		this.slider = new Slider({
			el: this.el,
			startIndex: this.currentCardIndex || 0,
			plugins: {
				responsive: {
					maxShowItems: 4
				},
				keyboard: {},
				touch: {
					touchEl: '#singleCardHolder',
					enableTap:false,
					enableSwipe:true
				}
			}
		});

		this.initNav();
		this.initListeners();
	};

	// Delegate and augment slider goTo methods 
	$.each(['goToNext', 'goToPrev', 'goToFirst', 'goToLast', 'goToCurrent'], function(index, method) {
		DeckSlider.prototype[method] = function() {
			return this.slider[method].apply(this.slider, arguments);
		};
	});

	// Delegate methods to slider as-is 
	$.each(['isLastItem'], function(index, method) {
		DeckSlider.prototype[method] = function() {
			return this.slider[method]();
		};
	});

	// Initializes the navigation buttons.
	DeckSlider.prototype.initNav = function() {
		var self = this;
		var navButtons = {
			"#first_card": "goToFirst",
			"#previous_card": "goToPrev",
			"#next_card": "goToNext",
			"#last_card": "goToLast",
			".mobileFirst": "goToFirst",
			".mobilePrevious": "goToPrev",
			".mobileNext": "goToNext",
			".mobileLast": "goToLast"
		};

		$.each(navButtons, function(key, value) {
			$(key).on("click", function(evt) {
				evt.preventDefault();
				self[value]();

			});
		});
	};

	// Initializes listeners on card elements and the slider object.
	DeckSlider.prototype.initListeners = function() {
		this.slider.bind("beforeslide", this.onBeforeSlide);
		this.slider.bind("slide", this.onSlide);
		this.el.on("click", ".card", this.onClickCard);
	};

	// Triggers load for batch of cards.
	DeckSlider.prototype.triggerLoad = function(index) {
		var card_ids = []; 
		var buf_size = 2;
		var buf_pos = index % this.loadSize;
		var is_card_loaded = (this.loaded[this.card_ids[index]] ? true : false);
		var load = false;
		var i, len, card_id;

		if(buf_pos == buf_size || !is_card_loaded) {
			load = true;
		} else if(is_card_loaded) {
			load = false;
		}

		if(load) {
			for(i = 0, len = this.loadSize + buf_size; i < len; i++) {
				card_id = this.card_ids[index + i];
				if(card_id) {
					card_ids.push(card_id);
					this.loaded[card_id] = true;
				}
			}
			this.trigger("load", this, card_ids);
		}
	};

	// Handles slider event triggered before the slide.
	DeckSlider.prototype.onBeforeSlide = function(slider, fromIndex, toIndex) {
		var card_id = this.card_ids[fromIndex];
		this.trigger("beforeslide", this, {fromIndex:fromIndex, toIndex:toIndex, card_id:card_id});
	};

	// Handles slider event triggered after the slide.
	DeckSlider.prototype.onSlide = function(slider, index) {
		var card_id = this.card_ids[index];
		this.selectCard(card_id);
		this.triggerLoad(index);
		this.trigger("slide", this, {index:index, card_id:card_id});
	};

	// Handles a click on a card element.
	DeckSlider.prototype.onClickCard = function(e) {
		var card_id, currentTarget = e.currentTarget;
		if(this.isCard(currentTarget)) {
			card_id = this.getCardId(currentTarget);
			this.goToCard(card_id);
			return false;
		}
	};

	// Finds a card element by the card ID.
	DeckSlider.prototype.findByCardId = function(card_id) {
		return $(".card[data-card-id="+card_id+"]", this.el);
	};

	// Finds all the card IDs from the card elements.
	DeckSlider.prototype.findCardIds = function() {
		var self = this, cards = [];
		$(this.el).find(".card").each(function(index, el) {
			cards.push(self.getCardId(el));
		});
		return cards;
	};

	// Returns the card ID from an element.
	DeckSlider.prototype.getCardId = function(el) {
		return $(el).data("card-id");
	};

	// Returns the current card ID.
	DeckSlider.prototype.getCurrentCardId = function() {
		return this.currentCardId;
	};

	// Returns the current card number.
	DeckSlider.prototype.getCurrentCardNum = function() {
        var card = this.findByCardId(this.getCurrentCardId());
		return card.data('card-num');
	};
	DeckSlider.prototype.getCurrentCardIndex = function() {
        var card = this.getIndexOfCard(this.getCurrentCardId());
		return card+1;
	};

	// Returns true if the element is a card, false otherwise.
	DeckSlider.prototype.isCard = function(el) {
		return $(el).is(".card");
	};

	// Returns the total number of items in the slider.
	DeckSlider.prototype.getNumItems = function() {
		return this.slider.getNumItems();
	};

	// Returns the index of a card or 0 if not found.
	DeckSlider.prototype.getIndexOfCard = function(cardId) {
		var index = this.card_ids.indexOf(cardId);
		if(index >= 0) {
			return index;
		}
		return 0;
	};

	// Selects and highlights the given card. 
	DeckSlider.prototype.selectCard = function(card_id) {
		this.unhighlight();
		this.setCurrentCard(card_id);
		this.highlight();
	};

	// Advances the slider to the card with the given card ID.
	DeckSlider.prototype.goToCard = function(card_id) {
		var card_index = this.card_ids.indexOf(card_id);

		if(card_index !== -1) {
			this.slider.goTo(card_index);
		}
	};

	// Sets the current card by ID.
	DeckSlider.prototype.setCurrentCard = function(card_id) {
		this.currentCardId = card_id;
		this.currentCardEl = this.findByCardId(card_id);
		this.currentCardIndex = this.getIndexOfCard(card_id);
	};

	// Unhighlights the current card.
	DeckSlider.prototype.unhighlight = function() {
		if(this.currentCardEl) {
			this.currentCardEl.removeClass("card-clicked");
		}
	};

	// Highlights the current card.
	DeckSlider.prototype.highlight = function() {
		if(this.currentCardEl) {
			this.currentCardEl.addClass("card-clicked");
		}
	};

	// Shuffles all the cards.
	DeckSlider.prototype.shuffle = function() {
		var cards  = $(this.el).find("ul#cards");
		var child = cards.children();
		var random_index = -1;

		while (child.length) {
			random_index = Math.floor(Math.random() *  child.length);
			this.card_ids.push(this.card_ids.splice(random_index, 1)[0]);
			cards.append(child.splice(random_index, 1));
		}
		this.loaded = {};
		this.trigger("shuffle");
	};

    DeckSlider.prototype.reset = function(){
		var $cards  = $(this.el).find("ul#cards");

        $cards.find('.card').sort(function (a, b) {
            return +a.getAttribute('data-card-num') - +b.getAttribute('data-card-num');
        })
        .appendTo( $cards );
        this.card_ids = this.card_ids.sort(function(a, b){return a-b});
		this.loaded = {};
		this.trigger("shuffle");
    }
	// Plays the slider (i.e. auto-advance to the next card).
	DeckSlider.prototype.play = function(doneCallback) {
		this._playIntervalId = window.setInterval(this._play(doneCallback), this.playbackDelay);
	};

	// Helper method (private) to play the slider.
	DeckSlider.prototype._play = function(doneCallback) {
		return $.proxy(function() {
			var isNext = this.goToNext();
			var pause = !isNext || this.isLastItem();
			if(pause) {
				this.pause();
				doneCallback();
			}
		}, this);
	};

	// Pauses the slider playback.
	DeckSlider.prototype.pause = function() {
		if(this._playIntervalId !== null) {
			window.clearInterval(this._playIntervalId);
			this._playIntervalId = null;
		}
	};

	MicroEvent.mixin(DeckSlider); // augment prototype with event emitter functionality

    return DeckSlider;
});
