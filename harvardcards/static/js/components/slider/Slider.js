define([
	'jquery',
	'microevent',
	'components/slider/ResponsiveSliderPlugin',
	'components/slider/TouchSliderPlugin',
	'components/slider/KeyboardSliderPlugin',
 ], function(
	$,
	MicroEvent,
	ResponsiveSliderPlugin,
	TouchSliderPlugin,
	KeyboardSliderPlugin
) {

	/**
	 * The Slider class has the responsibility of knowing how to slide
	 * elements in a list left or right. It has no knowledge about the behavior
	 * of the individual items, nor should it. 
	 *
	 * This is intended to be used and configured by more specific slider classes. Plugins
	 * are one of the means by which the core slider functionality can be extended. A plugin
	 * is just an object that implements an "init(slider)" method. The plugin may then 
	 * use the public API of the slider to change its behavior and look and feel.
	 *
	 * The markup expected by the slider is just an unordered HTML list. The slider only
	 * checks for the presence of the list "ul" and its children, the "li" list items. 
	 * The contents of each list item is of no concern to the slider. It does not and 
	 * should not depend on anything inside the list item.
	 *
	 * Usage:
	 *		<div class="slider">
	 *			<ul> 
	 *				<li><a href="#">Foo</a></li>
	 *				<li><a href="#">Bar</a></li>
	 *			</ul>
	 *		</div>
	 *
	 *		<script>
	 *		var slider = new Slider({ 
	 *			el: $(".slider"), 
	 *			plugins: {
	 *				responsive: { 
	 *					maxShowItems: 4
	 *				},
	 *				touch: null,
	 *				keyboard: null
	 *			}
	 *		});
	 *		</script>
	 */
	var Slider = function(config) {
		this.el = config.el; // element to bind the slider to
		this.plugins = config.plugins || {}; // list of plugin names

		this.containerEl = null; // should be <ul>
		this.items = []; // should be <li>'s
		this.pluginMap = {}; // map of plugin instances
		this.currentIndex = config.startIndex || 0; // starting position
		this.slideWindow = 0; // number of items to show
		this.slideAmount = 0; // amount to slide
		this.slideUnit = '%'; // slide unit

		this.init();
	};

	// Defines the list of available plugins.
	// Maps plugin keys to constructors.
	Slider.pluginRegistry = {
		'touch': TouchSliderPlugin,
		'keyboard': KeyboardSliderPlugin,
		'responsive': ResponsiveSliderPlugin
	};

	// Initializes the slider.
	Slider.prototype.init = function() {
		var items = [];

		this.containerEl = $(this.el).find("ul").first();
		this.containerEl.children("li").each(function(index, el) {
			items.push(el);
		});
		this.items = items;

		if(this.items.length > 0 && !this.isValidIndex(this.currentIndex)) {
			throw new Error("invalid starting index");
		}

		this.initPlugins();
	};

	// Initializes all plugins, if any.
	Slider.prototype.initPlugins = function() {
		_.each(this.plugins, function(pluginConfig, pluginName) {
			var plugin, pluginClass = Slider.pluginRegistry[pluginName];
			if(!pluginClass) {
				throw new Error("invalid plugin: " + pluginName);
			}
			plugin = new pluginClass(pluginConfig);
			plugin.init(this);
			this.pluginMap[pluginName] = plugin;
		}, this);
	};

	// Go to (i.e. slide) to an item.
	// Triggers "beforeslide" and "slide" on success.
	// Returns true on success, false otherwise.
	Slider.prototype.goTo = function(index) {
		if(!this.isValidIndex(index)) {
			return false;
		}
		this.trigger("beforeslide", this, this.currentIndex, index);
		this._slide(index);
		this.currentIndex = index;
		this.trigger("slide", this, index);

		return true;
	};

	// Returns true if the slider advanced to the next item, false otherwise.
	Slider.prototype.goToNext = function() {
		if(this.currentIndex < this.getNumItems() - 1) {
			return this.goTo(this.currentIndex + 1);
		}
		return false;
	};

	// Returns true if the slider advanced to the previous item, false otherwise.
	Slider.prototype.goToPrev = function() {
		if(this.currentIndex > 0) {
			return this.goTo(this.currentIndex - 1);
		}
		return false;
	};

	// Returns true if the slider advanced to the first item, false otherwise.
	Slider.prototype.goToFirst = function() {
		return this.goTo(0);
	};

	// Returns true if the slider advanced to the last item, false otherwise.
	Slider.prototype.goToLast = function() {
		return this.goTo(this.getNumItems() - 1);
	};

	// Returns true if the slider advanced to the current item, false otherwise.
	Slider.prototype.goToCurrent = function() {
		return this.goTo(this.currentIndex);
	};

	// Returns true if the slider is on the last item, false otherwise.
	Slider.prototype.isLastItem = function() {
		return this.currentIndex === this.getLastIndex();
	};

	// Returns true if the slider is on the first item, false otherwise.
	Slider.prototype.isFirstItem = function() {
		return this.currentIndex === 0;
	};

	// Returns true if the index is valid, false otherwise.
	Slider.prototype.isValidIndex = function(index) {
		return index >= 0 && index < this.getNumItems();
	};

	// Returns the width of the slider element.
	Slider.prototype.getWidth = function() {
		return $(this.el).width();
	};

	// Returns the number of list items in the slider.
	Slider.prototype.getNumItems = function() {
		return this.items.length;
	};

	// Returns the last index of the slider's items.
	Slider.prototype.getLastIndex = function() {
		return this.items.length > 0 ? this.items.length - 1 : 0; 
	};

	// Returns the current index.
	Slider.prototype.getCurrentIndex = function() {
		return this.currentIndex;
	};

	// Sets the width of the slider element.
	Slider.prototype.setWidth = function(width) {
		this.el.style.width = width;
	};

	// Sets the slide value, which may be expressed as a percentage or in pixels.
	// Example: "100%" or "10px"
	Slider.prototype.setSlide = function(slide) {
		var amount = parseFloat(slide);
		var unit = slide.replace(amount, '');
		this.slideAmount = amount || 0;
		this.slideUnit =  unit || "%";
	};

	// Sets the slide window size. This is used to stop the slider 
	// from moving the window once it reaches the end.
	Slider.prototype.setWindow = function(windowSize) {
		if(windowSize >= 0 && windowSize < this.getNumItems()) {
			this.slideWindow = windowSize;
		}
	};

	// Helper function to slide to the given index.
	Slider.prototype._slide = function(index) {
		var position, limit;
		if(this.slideWindow) {
			limit = this.getNumItems() - this.slideWindow;
			if(index > limit) {
				index = limit;
			}
		}
		position = this._position(index);

		$(this.containerEl)[0].style.left = position;
	};

	// Helper function to return the CSS offset amount for the slide.
	Slider.prototype._position = function(index) {
		return '-' + (this.slideAmount * index) + this.slideUnit;
	};

	// Makes slider instances event emitters
	MicroEvent.mixin(Slider);


	return Slider;
});
