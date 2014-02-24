define(['jquery'], function($) {

var ArrowToggle = function(targetSelectorExpand, targetSelectorCollapse) {

	var expandAction = function() {
		var $el = $(this).is('a.arrowExpand') ? $(this) : $(this).find('a.arrowExpand');
		var $ulDeckMenu = $el.next();
		if(!$ulDeckMenu.hasClass('openDeckMenu')) {
		   $ulDeckMenu.toggle();
		   $el.hide();
		   //adds the class that positions the open deck menu
		   //inside the deck
		   $ulDeckMenu.addClass('openDeckMenu');
		}
		return false;
	};
 
	var collapseAction = function() {
		var $el = $(this).is('a.arrowCollapse') ? $(this) : $(this).find('a.arrowCollapse');
		var $ulDeckMenu = $el.parent().parent();
		if($ulDeckMenu.hasClass('openDeckMenu')) {
		   $ulDeckMenu.toggle();
		   $el.parent().parent().parent().find('a.arrowExpand').show();
		   //closes the admin menu by removing the css class that opens it
		   $ulDeckMenu.removeClass('openDeckMenu');
		}
		return false;
	};

	// Make sure this is wrapped in a $(document).ready()...
	return function() {
		$('a.arrowExpand').click(expandAction);
		$('a.arrowCollapse').click(collapseAction);
		$(targetSelectorExpand).on({
			'mouseenter': expandAction,
		});
		$(targetSelectorCollapse).on({
			'mouseleave': collapseAction
		});
	};
};

var exports = {
	Slider: Slider,
	ArrowToggle: ArrowToggle
};

return exports;

});
