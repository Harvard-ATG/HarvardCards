define(['jquery', 'components/slider/CollectionSlider'], function($, CollectionSlider) {
/*
	var sliders = {'decks':[],'templates':[]}; 
	var sliderLength;

	$('.slider').each(function() {
		var slider_type = $(this).data('slider-type');
			if ($(this).text() != ''){
					//create Slider objects
					sliders[slider_type].push(new Slider(this));
			}        
	});

	$(window).on("resize", function () {
		for(var k in sliders) {
			if(sliders.hasOwnProperty(k)) {
				sliderLength = sliders[k].length;
				if (sliderLength > 0) {
						for( var i=0; i < sliderLength; i++ ) {
								if ($('.sliderNav').css('display') == 'none' && !(typeof(window.ontouchstart) != 'undefined' || typeof(window.onmspointerdown) != 'undefined') )
								{
										sliders[k][i].resetUL(); //removing the size when going back into the noslider div
								} else {
										sliders[k][i].respond();
								}
						}
				}
			}
		}
	}).resize();
*/

	window.sliders = {'decks': [], 'templates': []};
	$('.slider').each(function(index, el) {
		window.sliders.decks.push(new CollectionSlider(this));
	});


	return {initModule: function(){}};
});
