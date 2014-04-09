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
		this.el = config.el;
		this.plugins = config.plugins || {};

		this.items = [];
		this.currentIndex = config.startIndex || 0;
		this.maxSlideIndex = 0;
		this.slideAmount = 0;
		this.slideUnit = '%';

		this.init();
	};

	Slider.prototype.pluginMap = {
		'responsive': ResponsiveSliderPlugin,
		'keyboard': KeyboardSliderPlugin,
		'touch': TouchSliderPlugin
	};

	Slider.prototype.init = function() {
		var items = [];

		this.container = $("ul", this.el).first();
		this.container.children("li").each(function(index, el) {
			items.push(el);
		});
		this.items = items;

		this.initPlugins();
	};

	Slider.prototype.initPlugins = function() {
		_.each(this.plugins, function(pluginConfig, pluginName) {
			var pluginClass = this.pluginMap[pluginName];
			var plugin = new pluginClass(pluginConfig);
			plugin.init(this);
		}, this);
	};

	Slider.prototype.goTo = function(index) {
		if(typeof index !== 'number') {
			throw new Error("index must be a number");
		} 
		if(index < 0 || index > this.getNumItems() - 1) {
			return false;
		}

		this.trigger("beforeslide", this, this.currentIndex);
		this._slide(index);
		this.currentIndex = index;
		this.trigger("slide", this, index);

		return true;
	};

	Slider.prototype.goToNext = function() {
		if(this.currentIndex < this.getNumItems() - 1) {
			return this.goTo(this.currentIndex + 1);
		}
		return false;
	};

	Slider.prototype.goToPrev = function() {
		if(this.currentIndex > 0) {
			return this.goTo(this.currentIndex - 1);
		}
		return false;
	};

	Slider.prototype.goToFirst = function() {
		return this.goTo(0);
	};

	Slider.prototype.goToLast = function() {
		return this.goTo(this.getNumItems() - 1);
	};

	Slider.prototype.goToCurrent = function() {
		return this.goTo(this.currentIndex);
	};

	Slider.prototype.isLastItem = function() {
		return this.currentIndex === this.getLastIndex();
	};

	Slider.prototype._slide = function(index) {
		var position;
		if(index > this.maxSlideIndex) {
			index = this.maxSlideIndex;
		}
		position = this._position(index);

		$(this.container)[0].style.left = position;
	};

	Slider.prototype._position = function(index) {
		return '-' + (this.slideAmount * index) + this.slideUnit;
	};

	Slider.prototype.getWidth = function() {
		return $(this.el).width();
	};

	Slider.prototype.getNumItems = function() {
		return this.items.length;
	};

	Slider.prototype.getLastIndex = function() {
		return this.items.length > 0 ? this.items.length - 1 : 0; 
	};

	Slider.prototype.getCurrentIndex = function() {
		return this.currentIndex;
	};

	Slider.prototype.setWidth = function(width) {
		this.el.style.width = width;
	};

	Slider.prototype.setSlide = function(slide) {
		var amount = parseFloat(slide);
		var unit = slide.replace(amount, '');
		this.slideAmount = amount || 0;
		this.slideUnit =  unit || "%";
	};

	Slider.prototype.setMaxSlideIndex = function(index) {
		this.maxSlideIndex = index;
	};

	MicroEvent.mixin(Slider);

	return Slider;
});
