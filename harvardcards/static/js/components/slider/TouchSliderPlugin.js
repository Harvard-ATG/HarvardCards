define(['jquery'], function($) {

    var TouchSliderPlugin = function() {

    };

    TouchSliderPlugin.prototype.init = function(slider) {
        this.slider = slider;
        //console.log("touch");
    };

	return TouchSliderPlugin;
});