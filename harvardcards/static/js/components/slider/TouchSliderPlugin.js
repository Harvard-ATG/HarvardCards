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

	var TouchSliderPlugin = function() {
		this.handleTouchEvents = $.proxy(this.handleTouchEvents, this);
	};

	TouchSliderPlugin.prototype.init = function(slider) {
		console.log("touch");
		this.slider = slider;
		this.attachTouchEvents();
	};

	TouchSliderPlugin.prototype.hideNav = function() {
		if (typeof(window.ontouchstart) != 'undefined' || typeof(window.onmspointerdown) != 'undefined') {
			this.slider.hideNav(); //$('.sliderNav').hide();
		}
	};

	TouchSliderPlugin.prototype.attachTouchEvents = function() {
		$(this.slider.el).on("touchmove touchstart touchend", this.handleTouchEvents);
	};

	TouchSliderPlugin.prototype.handleTouchEvents = function(evt) {
		var e = evt.originalEvent;
		var direction = 0;
		var scrollTop = false;
        var $parentEl = $(this.slider.el).parent();
		var index = $parentEl.index();

		console.log("touch event", evt.type, "index", index, "event object", evt);

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

	TouchSliderPlugin.prototype.scrollTop = function(scrollTop) {
		var duration = 500;
		if(typeof scrollTop === 'number') {
			$('html body').animate({scrollTop: scrollTop}, duration);
		}
	};

	TouchSliderPlugin.prototype.cleanTransitions = function(node) {
		node.style[TRANSITION] = 'none';
	};

	TouchSliderPlugin.prototype.setPosition = function(node, left) {
		node.style[TRANSFORM] =  "translate3d("+left+"px, 0, 0)";
	};



	return TouchSliderPlugin;
});
