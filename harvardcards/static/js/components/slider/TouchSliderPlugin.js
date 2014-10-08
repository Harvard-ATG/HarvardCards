define(['jquery'], function($) {

	var TRANSITION  = 'transition';
	var TRANSFORM   = 'transform';
	var TRANSITION_END = 'transitionend';
	var TRANSFORM_CSS  = 'transform';
	var TRANSITION_CSS = 'transition';

	if (typeof document.body.style.webkitTransform !== undefined) {
		TRANSITION = 'webkitTransition';
		TRANSFORM = 'webkitTransform';
		TRANSITION_END = 'webkitTransitionEnd';
		TRANSFORM_CSS = '-webkit-transform';
		TRANSITION_CSS = '-webkit-transition';
	}
	/**
	 * TouchSliderPlugin responsible for adding ability to advance
	 * the slider using swipe left/right or up/down.
	 *
	 * This class isn't meant to be instantiated by itself. Collaborates
	 * With Slider.
	 *
	 * Usage:
	 *      var plugin = new TouchSliderPlugin();
	 *      plugin.init(slider);
	 */
	var TouchSliderPlugin = function(config) {
		config = config || {};
		this.config = config;
		this.handleTouchEvents = $.proxy(this.handleTouchEvents, this);
	};

	// Initializes the plugin.
	TouchSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
		this.touchEl = this.config.touchEl || this.slider.el;
		if(this.hasTouchSupport()) {
			this.hideNav();
			this.attachTouchEvents();
		}
	};

	// Returns true if the device has touch support, false otherwise.
	TouchSliderPlugin.prototype.hasTouchSupport = function() {
		return 'ontouchstart' in document.documentElement;
	};

	// Hides the navigation element.
	TouchSliderPlugin.prototype.hideNav = function() {
		$(".sliderNav", this.slider.el).hide();
	};

	// Attaches touch event handles to the slider.
	TouchSliderPlugin.prototype.attachTouchEvents = function() {
		$(this.touchEl).on("touchmove touchstart touchend", this.handleTouchEvents);
	};

	// Handler for touch events.
	TouchSliderPlugin.prototype.handleTouchEvents = function(evt) {
		var e = evt.originalEvent;
		var swipeWidth = 50; 
		var x, y;

		//console.log("touch event", evt.type, "event object", evt, "touches", e.touches, "onetouch", e.touches[0]);

		switch(e.type) {
			case 'touchstart':
				x = e.touches[0].clientX;
				y = e.touches[0].clientY;
				this.startPos = {x:x,y:y};
				this.lastPos = {x:x,y:y};
				break;
			case 'touchmove':
				x = e.touches[0].clientX;
				y = e.touches[0].clientY;
				this.lastPos = {x:x,y:y};
				//console.log("touchmove", x, y, "last", this.lastPos.x, this.lastPos.y);
				break;
			case 'touchend':
				if(this.lastPos.x - this.startPos.x > swipeWidth) {
					this.slider.goToPrev();
				} else if(this.lastPos.x - this.startPos.x < -swipeWidth) {
					this.slider.goToNext();
				}
				break;
			default:
				//console.log("touch event not handled", e.type);
				break;
		}

		return true;
	};

	// Helper function to scroll the screen.
	TouchSliderPlugin.prototype.scrollTop = function(scrollTop) {
		var duration = 500;
		if(typeof scrollTop === 'number') {
			$('html body').animate({scrollTop: scrollTop}, duration);
		}
	};

	// Not used.
	TouchSliderPlugin.prototype.cleanTransitions = function(node) {
		node.style[TRANSITION] = 'none';
	};

	// Not used.
	TouchSliderPlugin.prototype.setPosition = function(node, left) {
		node.style[TRANSFORM] =  "translate3d("+left+"px, 0, 0)";
	};



	return TouchSliderPlugin;
});
