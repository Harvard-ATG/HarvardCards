define(['jquery', 'components/slider/Slider'], function($, Slider) {

	var CollectionSlider = function(el) {
		this.el = $(el);
		this.init();
	};

	CollectionSlider.prototype.init = function() {
		this.slider = new Slider({
			el: this.el,
			plugins: {'responsive':null, 'touch':null}
		});
	};

	// Delegate methods to Slider instance
	$.each(['goToNext', 'goToPrev'], function(index, method) {
		CollectionSlider.prototype[method] = function() {
			this.slider[method]();
		};
	})

    return CollectionSlider;
});
