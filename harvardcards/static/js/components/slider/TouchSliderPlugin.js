define(['jquery'], function($) {

	var TRANSITION     = 'transition',
        TRANSFORM      = 'transform',
        TRANSITION_END = 'transitionend',
        TRANSFORM_CSS  = 'transform',
        TRANSITION_CSS = 'transition';

    if (typeof document.body.style.webkitTransform !== undefined) {
        TRANSITION = 'webkitTransition';
        TRANSFORM = 'webkitTransform';
        TRANSITION_END = 'webkitTransitionEnd';
        TRANSFORM_CSS = '-webkit-transform';
        TRANSITION_CSS = '-webkit-transition';
    }

	function cleanTransitions(node)
	{
            node.style[TRANSITION] = 'none';
    }

	function setPosition(node, left)
	{
        node.style[TRANSFORM] =  "translate3d("+left+"px, 0, 0)";
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
		var scrollTop = 0;
		var i = $(this.slider.el).parent().index();

		console.log("touch event", evt.type, "index", i, "event object", evt);

		if (e.type == 'touchstart') {
			this.startPos = e.touches[0].clientX;
			this.lastPos = this.startPos;
			direction = 0;

			this.startPosY = e.touches[0].clientY;
			this.lastPosY = this.startPosY;
		} else if (e.type == 'touchmove') {
			e.preventDefault();
			if (this.lastPos > this.startPos) {
				direction = -1;
			} else {
				direction = 1;
			}

			this.lastPosY = e.touches[0].clientY;
			this.lastPos = e.touches[0].clientX;

			//console.log('last down: ' + lastPosY);

		} else if (e.type == 'touchend') {
            if(this.lastPosY - this.startPosY > 50) {
				i--;
				if(i <= 0) {
					//first slider scroll to top of page
					scrollTop = $('html').position().top;
				} else {
					//page up
					scrollTop = $(this.slider.el).parent().prev().position().top;
				}
		        this.scrollTop(scrollTop);
            } else if (this.lastPosY - this.startPosY < -50) {
            	i++;
            	console.log('index ' + i);
            	if (i >= this.slider.getNumItems()) {
            		//first slider scroll to top of page
		            scrollTop = $('html').position().bottom;
            	} else {
	            	//page down
		            scrollTop = $(this.slider.el).parent().next().position().top;
            	}
	            this.scrollTop(scrollTop);
            	console.log('index End = ' + i)
            } else {
	            if(this.lastPos - this.startPos > 100) {
	                this.slider.goToPrev();
	            } else if(this.lastPos - this.startPos < -100) {
	                this.slider.goToNext();
	            }
            }
		}
		return false;
	};

	TouchSliderPlugin.prototype.scrollTop = function(scrollTop) {
		if(scrollTop) {
			$('html body').animate({scrollTop: scrollTop}, 500);
		}
	};

	return TouchSliderPlugin;
});