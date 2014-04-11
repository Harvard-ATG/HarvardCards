define(['jquery'], function($) {
    
	/**
	 * ResponsiveSliderPlugin responsible for modifying the layout of the
	 * slider to best fit the screen. That is, it makes the slider responsive.
	 *
	 * This class isn't meant to be instantiated by itself. Collaborates
	 * With Slider.
	 *
	 * Usage:
	 *      var plugin = new ResponsiveSliderPlugin();
	 *      plugin.init(slider);
	 */
	var ResponsiveSliderPlugin = function(config) {
		config = config || {};
		this.hasLayout = false;
		this.maxShowItems = config.maxShowItems || null;
		this.layout = {}; // holds layout configuration
		this.resize = $.proxy(this.resize, this);
	};

    // Initializes the plugin.
	ResponsiveSliderPlugin.prototype.init = function(slider) {
		this.slider = slider;
		this.resize();
		this.initListeners();
	};

    // Initializes listeners.
	ResponsiveSliderPlugin.prototype.initListeners = function() {
		$(window).on("resize", this.resize);
	};

    // Resizes the slider if necessary.
	ResponsiveSliderPlugin.prototype.resize = function() {
		this.loadLayout();
		this.doLayout();
	};

    // List of rules for configuring the layout. 
	// For reference:
	//   iphone portrait   = screen and (min-width: 320px)
	//   iphone landscape  = screen and (min-width: 480px)
	//   ipad portrait     = screen and (min-width: 768px)
	//   desktop           = screen and (min-width: 1024px)
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

    // Loads a layout that will adapt to the screen. Uses media query rules
    // to configure the layout. The first media query that matches from
    // the rules will be loaded.
	ResponsiveSliderPlugin.prototype.loadLayout = function() {
		var i, rule, len, matched = false;

		this.hasLayout = false;
		this.layout = {};

		for(i = 0, len = this.rules.length; i < len; i++) {
			rule = this.rules[i];
			matched = this.checkMediaQuery(rule.mediaQuery);
			if(rule.showItems === this.maxShowItems) {
				matched = true;
			}
			if(matched) {
				this.hasLayout = true;
				this.layoutHandler = rule.handler;
				this.showItems = rule.showItems;
				break;
			}
		}
	};

    // Checks if there is a layout and calls the corresponding handler,
    // otherwise just resets the layout.
	ResponsiveSliderPlugin.prototype.doLayout = function() {
		if(this.hasLayout) {
			this[this.layoutHandler]();
		} else {
			this.resetLayout();
		}
	};

    // Applies the current layout to the slider and its items
	ResponsiveSliderPlugin.prototype.applyLayout = function() {
		var layout = this.layout;
		var numItems = this.slider.getNumItems();

		$(this.slider.containerEl).width(layout.containerWidth);

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
		this.slider.setWindow(layout.slideWindow);
		this.slider.goToCurrent(); // keep position when layout changes
	};

    // Resets the layout to the default 
	ResponsiveSliderPlugin.prototype.resetLayout = function() {
		$(this.slider.containerEl).removeAttr('style');
		$(this.slider.items).removeAttr('style');
	};

    // Creates a layout for a single item
	ResponsiveSliderPlugin.prototype.singleLayout = function() {
		var showItems = this.showItems;
		var numItems = this.slider.getNumItems();
		var sliderWidth = this.slider.getWidth();
		var containerWidth = sliderWidth * numItems;
		var totalItemsBorderWidth = this.getItemBorderWidth() * numItems;

		this.layout.containerWidth = containerWidth;
		this.layout.itemWidth = (sliderWidth - 2) + "px";
		this.layout.itemMarginRight = 0;
		this.layout.slideWindow = showItems;
		this.layout.slide = "100%";

		this.applyLayout();
	};

    // Creates a layout for multiple items 
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
		this.layout.slideWindow = showItems;
		this.layout.slide = slide;

		this.applyLayout();
	};

    // Utility function to return the border width of the slider items. Returns
    // the number without units.
	ResponsiveSliderPlugin.prototype.getItemBorderWidth = function() {
		return parseFloat($(this.slider.items).css('border-left-width'));
	};

    // Utility function to execute a media query. Returns true if it matches, false otherwise.
	ResponsiveSliderPlugin.prototype.checkMediaQuery = function(mq) {
		var mediaQuery = window.matchMedia(mq);
		return mediaQuery.matches ? true : false;
	};
	
	return ResponsiveSliderPlugin;
});
