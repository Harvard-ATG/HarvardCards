define(['jquery', 'components/slider/Slider'], function($, Slider) {

	/**
	 * The CollectionSlider is responsible for displaying a list of 
	 * decks as a slider on smaller screen sizes.
	 *
	 * The slider is responsive to the size of the screen and supports
	 * touch events. Swipe left/right to go to the next/previous deck.
	 * Swipe up/down to go to the next collection.
	 *
	 * Usage:
	 *		var slider = new CollectionSlider($("#slider"));
	 *		slider.goToNext();
	 *		slider.goToPrev();
	 */
	var CollectionSlider = function(el) {
		this.el = $(el);
		this.goToNext = $.proxy(this.goToNext, this);
		this.goToPrev = $.proxy(this.goToPrev, this);
		this.init();
	};

	// Initializes the slider object. 
	CollectionSlider.prototype.init = function() {
		this.slider = new Slider({
			el: this.el,
			plugins: {'responsive':null, 'touch':null}
		});

		this.initNav();
	};

	// Initializes the nav buttons.
	CollectionSlider.prototype.initNav = function() {
		var self = this;
		var navButtons = {
			".sliderPrev": "goToPrev",
			".sliderNext": "goToNext"
		};

		$.each(navButtons, function(key, value) {
			$(".sliderNav", self.el).find(key).on("click", function(evt) {
				evt.preventDefault();
				self[value]();
			});
		});
	};

	// Adds methods to the CollectionSlider that just delegate to slider.
	// These methods are considered public.
	$.each(['goToPrev', 'goToNext'], function(index, method) {
		CollectionSlider.prototype[method] = function() {
			return this.slider[method]();
		};
	});

	return CollectionSlider;
});
