define(['jquery', 'components/slider/Slider'], function($, Slider) {

	var CollectionSlider = function(el) {
		this.el = $(el);
		this.goToNext = $.proxy(this.goToNext, this);
		this.goToPrev = $.proxy(this.goToPrev, this);
		this.init();
	};

	CollectionSlider.prototype.init = function() {
		this.slider = new Slider({
			el: this.el,
			plugins: {'responsive':null, 'touch':null}
		});

		this.initNav();
	};

	CollectionSlider.prototype.initNav = function() {
		var self = this;
		var navButtons = {
			".sliderPrev": "goToPrev",
			".sliderNext": "goToNext"
		};

		$.each(navButtons, function(key, value) {
			$(".sliderNav", self.el).find(key).on("click", function(evt) {
				evt.preventDefault();
				self.slider[value]();
			});
		});
	};

    return CollectionSlider;
});
