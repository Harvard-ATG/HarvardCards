define(['jquery', 'jquery.mousewheel'], function($) {

	var KeyboardSliderPlugin = function() {
		this.handleKeyPress = $.proxy(this.handleKeyPress, this);
		this.handleMouseWheel = $.proxy(this.handleMouseWheel, this);
	};

	KeyboardSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
		this.initListeners();
	};

	KeyboardSliderPlugin.prototype.initListeners = function() {
		$(document).on('keydown', this.handleKeyPress);
		$(document).mousewheel(this.handleMouseWheel);
	};

	KeyboardSliderPlugin.prototype.handleMouseWheel = function(e) {
		//console.log("mousewheel", e);
		if(e.deltaX > 0) {
			e.preventDefault();
			this.slider.goToNext();
		} else if(e.deltaX < 0) {
			e.preventDefault();
			this.slider.goToPrev();
		}
	};

	KeyboardSliderPlugin.prototype.handleKeyPress = function(e) {
		//console.log("keypress", e, e.keyCode);
		if (e.keyCode == 37) {
			this.slider.goToPrev();
		} else if (e.keyCode == 39) {
			this.slider.goToNext();
		}
	};

	return KeyboardSliderPlugin;
});
