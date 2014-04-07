define(['jquery'], function($) {
	var ResponsiveSliderPlugin = function() {
		this.hasLayout = false;
		this.layout = {};
		this.resize = $.proxy(this.resize, this);
	};

	ResponsiveSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
		this.resize();
		this.initListeners();
	};

	ResponsiveSliderPlugin.prototype.initListeners = function() {
		$(window).on("resize", this.resize);
	};

	ResponsiveSliderPlugin.prototype.resize = function() {
		this.loadLayout();
		this.doLayout();
	};

	//For reference:
	//  iphone portrait   = screen and (min-width: 320px)
	//  iphone landscape  = screen and (min-width: 480px)
	//  ipad portrait     = screen and (min-width: 768px)
	//  desktop           = screen and (min-width: 1024px)
	ResponsiveSliderPlugin.prototype.rules = [{
		"mediaQuery": "screen and (min-width: 280px) and (max-width: 320px)",
		"handler": "singleLayout",
		"showItems": 1
	},{
		"mediaQuery": "screen and (min-width: 321px) and (max-width: 480px)",
		"handler": "multiLayout",
		"showItems": 2
	},{
		"mediaQuery": "screen and (min-width: 481px) and (max-width: 680px)",
		"handler": "multiLayout",
		"showItems": 3
	},{
		"mediaQuery": "screen and (min-width: 680px) and (max-width: 1023px)",
		"handler": "multiLayout",
		"showItems": 4
	},{
		"mediaQuery": "screen and (min-width: 1024px)",
		"handler": "resetLayout",
		"showItems": null
	}];

	ResponsiveSliderPlugin.prototype.loadLayout = function() {
		var i, rule, len;

		this.hasLayout = false;
		this.layout = {};

		for(i = 0, len = this.rules.length; i < len; i++) {
			rule = this.rules[i];
			if(this.checkMediaQuery(rule.mediaQuery)) {
				this.hasLayout = true;
				this.layoutHandler = rule.handler;
				this.showItems = rule.showItems;
				break;
			}
		}
	};

	ResponsiveSliderPlugin.prototype.getItemBorderWidth = function() {
		return parseFloat($(this.slider.items).css('border-left-width'));
	};

	ResponsiveSliderPlugin.prototype.checkMediaQuery = function(mq) {
		var mediaQuery = window.matchMedia(mq);
		return mediaQuery.matches ? true : false;
	};

	ResponsiveSliderPlugin.prototype.doLayout = function() {
		if(this.hasLayout) {
			this[this.layoutHandler]();
		} else {
			this.resetLayout();
		}
	};

	ResponsiveSliderPlugin.prototype.applyLayout = function() {
		var layout = this.layout;
		var numItems = this.slider.getNumItems();

		$(this.slider.container).width(layout.containerWidth);

		$(this.slider.items).each(function(index, el) {
			el.style.width = layout.itemWidth;
			el.style.clear = "none";
			if(layout.itemMarginRight) {
				if(index < numItems - 1) {
					el.style.marginRight = layout.itemMarginRight;
				} else {
					el.style.marginRight = 0;
				}
			} else {
				el.style.marginRight = 0;
			}
		});

		this.slider.setSlide(layout.slide);
		this.slider.setSlideLimit(layout.slideLimit);
		this.slider.goToCurrent(); // keep position when layout changes
	};

	ResponsiveSliderPlugin.prototype.resetLayout = function() {
		$(this.slider.container).removeAttr('style');
		$(this.slider.items).removeAttr('style');
	};

	ResponsiveSliderPlugin.prototype.singleLayout = function() {
		var showItems = this.showItems;
		var numItems = this.slider.getNumItems();
		var sliderWidth = this.slider.getWidth();
		var containerWidth = sliderWidth * numItems;
		var totalItemsBorderWidth = this.getItemBorderWidth() * numItems;

		this.layout.containerWidth = containerWidth;
		this.layout.itemWidth = (sliderWidth - 2) + "px";
		this.layout.itemMarginRight = 0;
		this.layout.slideLimit = numItems - showItems;
		this.layout.slide = "100%";

		this.applyLayout();
	};

	ResponsiveSliderPlugin.prototype.multiLayout = function() {
		var showItems = this.showItems;
		var numItems = this.slider.getNumItems();
		var sliderWidth = this.slider.getWidth();
		var containerWidth = sliderWidth * numItems;
		var itemBorderWidth = this.getItemBorderWidth();
		var itemMargin = 30;
		var totalItemMargin = (showItems - 1) * itemMargin;
		var totalBorderWidth = showItems * (itemBorderWidth * 2);
		var itemWidth = Math.floor((sliderWidth - totalItemMargin - totalBorderWidth) / showItems);
		var slide = itemWidth + itemMargin + (itemBorderWidth * 2) + "px";

		this.layout.containerWidth = ((itemWidth + itemMargin + (itemBorderWidth * 2)) * numItems) - itemMargin + "px";
		this.layout.itemWidth =  itemWidth + "px";
		this.layout.itemMarginRight = itemMargin + "px";
		this.layout.slideLimit = numItems - showItems;
		this.layout.slide = slide;

		this.applyLayout();
	};
	
	return ResponsiveSliderPlugin;
});
