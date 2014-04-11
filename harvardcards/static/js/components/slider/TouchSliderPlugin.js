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
		this.handleTouchEvents = $.proxy(this.handleTouchEvents, this);
	};

	// Initializes the plugin.
	TouchSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
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
		$(this.slider.el).on("touchmove touchstart touchend", this.handleTouchEvents);
	};

	// Handler for touch events.
	TouchSliderPlugin.prototype.handleTouchEvents = function(evt) {
		var e = evt.originalEvent;
		var direction = 0;
		var scrollTop = false;
        var $parentEl = $(this.slider.el).parent();
		var index = $parentEl.index();

		//console.log("touch event", evt.type, "index", index, "event object", evt);

		switch(e.type) {
			case 'touchstart':
				this.startPos = e.touches[0].clientX;
				this.lastPos = this.startPos;
				direction = 0;
				this.startPosY = e.touches[0].clientY;
				this.lastPosY = this.startPosY;
				break;
			case 'touchmove':
				e.preventDefault();
				direction = (this.lastPos > this.startPos) ? -1 : 1;
				this.lastPosY = e.touches[0].clientY;
				this.lastPos = e.touches[0].clientX;
				//console.log('last down: ' + lastPosY);
				break;
			case 'touchend':
				if(this.lastPosY - this.startPosY > 50) {
					index--;
					if(index <= 0) {
						//first slider scroll to top of page
						scrollTop = $('html').position().top;
					} else {
						//page up
						if($parentEl.prev().position()) {
							scrollTop = $parentEl.prev().position().top;
						}
					}
					this.scrollTop(scrollTop);
				} else if (this.lastPosY - this.startPosY < -50) {
					index++;
					if (index >= this.slider.getNumItems()) {
						//first slider scroll to top of page
						scrollTop = $('html').position().bottom;
					} else {
						//page down
						if($parentEl.next().position()) {
							scrollTop = $parentEl.next().position().top;
						}
					}
					this.scrollTop(scrollTop);
				} else {
					if(this.lastPos - this.startPos > 100) {
						this.slider.goToPrev();
					} else if(this.lastPos - this.startPos < -100) {
						this.slider.goToNext();
					}
				}
				break;
			default:
				//console.log("touch event not handled", e.type);
				break;
		}
		return false;
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
