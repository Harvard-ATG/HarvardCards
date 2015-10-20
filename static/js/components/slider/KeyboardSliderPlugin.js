define(['jquery'], function($) {

	/**
	 * KeyboardSliderPlugin responsible for adding ability to advance
	 * the slider using keyboard left/right arrows or the mouse wheel.
	 *
	 * This class isn't meant to be instantiated by itself. Collaborates
	 * With Slider.
	 *
	 * Usage:
	 *      var plugin = new KeyboardSliderPlugin();
	 *      plugin.init(slider);
	 */
	var KeyboardSliderPlugin = function(config) {
		config = config || {};
		this.handleKeyPress = $.proxy(this.handleKeyPress, this);
		this.handleMouseWheel = $.proxy(this.handleMouseWheel, this);
	};

	// Initializes the plugin.
	KeyboardSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
		this.initListeners();
	};

	// Initializes listeners.
	KeyboardSliderPlugin.prototype.initListeners = function() {
		$(document).on('keydown', this.handleKeyPress);

		//------------------------------------------------------------
		// **NOTE** 
		// Disabled mousewheel handler that advanced the slider next/prev
		// because it interfered with two-finger scrolling behavior on 
		// trackpads. Two-finger scrolling should be preserved.
		//     -abarrett 12/14/14
		//------------------------------------------------------------
		//$(document).mousewheel(this.handleMouseWheel);
	};

	// Handles the mousewheel event.
	// NOTE: This function is not used anymore. See initListiners().
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

	// Handles the keypress event.
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
