define([
	'jquery',
	'microevent',
	'components/slider/ResponsiveSliderPlugin',
	'components/slider/TouchSliderPlugin'
 ], function(
	$,
	MicroEvent,
	ResponsiveSliderPlugin,
    TouchSliderPlugin
) {

	var Slider = function(config) {
        this.el = config.el;
        this.plugins = config.plugins || [];

		this.items = [];
        this.currentIndex = 0;
        this.slideAmount = 0;
		this.slideLimit = 0;
        this.slideUnit = '%';

        this.init();
	};

    Slider.prototype.pluginMap = {
        'responsive': ResponsiveSliderPlugin,
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
        _.each(this.plugins, function(pluginName) {
            var pluginClass = this.pluginMap[pluginName];
            var plugin = new pluginClass();
            plugin.init(this);
        }, this);
    };

    Slider.prototype.goTo = function(index) {
        if(typeof index !== 'number') {
            throw new Error("index must be a number");
        } else if(index < 0 || index > this.getNumItems() - 1) {
            throw new Error("index out of bounds");
        }

	    if(this._canSlide(index)) {
            this._slide(this._slidePosition(index));
	    }
        this.currentIndex = index;
    };

    Slider.prototype.goToNext = function() {
        if(this.currentIndex < this.getNumItems() - 1) {
            this.goTo(this.currentIndex + 1);
        }
    };

    Slider.prototype.goToPrev = function() {
        if(this.currentIndex > 0) {
            this.goTo(this.currentIndex - 1);
        }
    };

    Slider.prototype.goToFirst = function() {
        this.goTo(0);
    };

    Slider.prototype.goToLast = function() {
        this.goTo(this.numItems - 1);
    };

	Slider.prototype.goToCurrent = function() {
		this.goTo(this.currentIndex);
	};

	Slider.prototype._canSlide = function(to) {
		return to <= this.slideLimit;
	};

    Slider.prototype._slide = function(position) {
        $(this.container)[0].style.left = position;
    };

    Slider.prototype._slidePosition = function(index) {
        return '-' + (this.slideAmount * index) + this.slideUnit;
    };

	Slider.prototype.getWidth = function() {
		return $(this.el).width();
	};

	Slider.prototype.getNumItems = function() {
		return this.items.length;
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

	Slider.prototype.setSlideLimit = function(limit) {
		this.slideLimit = limit;
	};

	return Slider;
});
