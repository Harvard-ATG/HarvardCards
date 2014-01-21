define(['jquery'], function($) {

var Slider = function() { this.initialize.apply(this, arguments) }
Slider.prototype = {

	initialize: function(slider,deckView) {
		//to force scroller on view and review modes thumbnails
		//regardles of monitor size. Homepage or "dashboard" set to false
		if (typeof deckView === "undefined")
		{
			this.deckView = false;
		}
		else
		{
			this.deckView = deckView;
		}
		
		this.ul = slider.children[0]
		if (!this.ul){
			return;
		}
		//set the li's
		this.li = this.ul.children
		//get the border width for the li's
		this.liborder = getCSSprop($(this.li),'border-left-width');
		
		this.currentIndex = 0

		//for ipad sliding, we want to set a cealing for clicks
		//so it stops at the last li and not click onto empty space 
		/*if ( checkMediaQuery("screen and (min-width: 768px)") ){
			this.deckView = true;
			this.liToShow = 4;
			this.slideWindow = 4;
		}else{
			this.liToShow = 3;
			this.slideWindow = 3;
		}*/
		
		this.totalLi = this.li.length;
		this.clickCealing;
		
		this.slideAmmount = 0;
		this.slideUnit = '%';
		
		//this.respond(); //this making the method go twice removed for now
		
		/*console.log(
			'this.currentIndex = ' + this.currentIndex + ' ' +
			'this.liborder = ' + this.liborder + ' ' +
			'this.deckView = ' + this.deckView + ' ' +
			'this.liToShow = ' + this.liToShow + ' ' +
			'this.slideWindow = ' + this.slideWindow + ' ' +
			'this.totalLi = ' + this.totalLi + ' ' +
			'this.clickCealing = ' + this.clickCealing + ' ' +
			'this.slideAmmount = ' + this.slideAmmount + ' ' +
			'this.slideUnit = ' + this.slideUnit
		);*/
		
	},

	goTo: function(index) {
		// filter invalid indices
		if (index < 0 || index > this.li.length - 1 || index - 1 == this.clickCealing )
		return
		
		// move <ul> left
		this.ul.style.left = '-' + (this.slideAmmount * index) + this.slideUnit;
		
		this.currentIndex = index;
		//console.log ('goTo: ' + this.currentIndex);
	},
	
	goToPrev: function() {
		this.goTo(this.currentIndex - 1)
		//console.log ('prev: ' + this.currentIndex);
	},
	
	goToNext: function() {
		this.goTo(this.currentIndex + 1)
		//console.log ('next: ' + this.currentIndex);
	},
	
	respond: function(){
		//iphone portrait	= screen and (min-width: 320px)
		//iphone landscape	= screen and (min-width: 480px)
		//ipad portrait		= screen and (min-width: 768px)
		//desktop			= screen and (min-width: 1024px)
		var oneCard = checkMediaQuery("screen and (min-width: 280px) and (max-width: 320px)");
		var twoCards = checkMediaQuery("screen and (min-width: 321px) and (max-width: 480px)");
		var threeCards = checkMediaQuery("screen and (min-width: 481px) and (max-width: 680px)");
		var fourCards = checkMediaQuery("screen and (min-width: 680px) and (max-width: 1023px)");
		var desktop = checkMediaQuery("screen and (min-width: 1024px)");
		
		var ulwidth, rspLiWidth, liMargin, ipad, liToShow, borderAmmount, slideWindow, respCards;
		respCards = false;
		if (twoCards)
		{
			liToShow = 2;
			slideWindow = 2;
			respCards = true;
		}
		else if(threeCards)
		{
			liToShow = 3;
			slideWindow = 3;
			respCards = true;
		}
		else if(fourCards || this.deckView)
		{
			liToShow = 4;
			slideWindow = 4;
			respCards = true;
		}
		
		//border width of scroller li
		borderAmmount = this.liborder;
			
		var sliderContext = $(this.ul).parent().width();
		//total list item
		var totalLI = this.li.length;
		//li's borders to get added to the ul width
		var liBorders = borderAmmount * totalLI;
		//set a li margin only to be use with ipad
		liMargin = 30;
		//li to show on ipad view
		//liToShow = this.liToShow;
		
		//var mq = window.matchMedia("(min-width: 768px) and (max-width: 1024px)");
		
		if (twoCards || threeCards || fourCards || this.deckView) //(mq.matches || this.deckView)
		{
			var respUnits = new RespondObj(sliderContext,liMargin,liToShow,this.totalLi,slideWindow, borderAmmount);
			/*console.log('sliderContext = ' + sliderContext);
			console.log('liMargin = ' + liMargin);
			console.log('liToShow = ' + liToShow);
			console.log('this.totalLi = ' + this.totalLi);
			console.log('this.slideWindow = ' + this.slideWindow);
			console.log('borderAmmount = ' + borderAmmount);
			console.log('deckView = ' + this.deckView);*/
			
			rspLiWidth = respUnits.rspLiWidthAndUnit;
			this.slideAmmount = respUnits.slideAmmount;
			this.slideUnit = respUnits.slideUnit;
			this.ul.style.width = respUnits.ulWidth;
			this.clickCealing = respUnits.clickCealing;
			//console.log('slideAmmount = ' + respUnits.slideAmmount);
			
			ipad = true;
			this.goTo(this.currentIndex);//stay in current index when flipping screen
		}
		else if (oneCard)
		{
			//give the UL a new width to accomodate all the li's plus their margins
			ulwidth = (sliderContext * totalLI);
			this.ul.style.width = ( ulwidth + liBorders ) + 'px';
			rspLiWidth = sliderContext-2 + 'px';//width of li
			//ammount to slide: in this 100 since ther is only one card
			this.slideAmmount = 100;
			this.slideUnit = '%';
			
			this.clickCealing = this.totalLi - 1;
			ipad = false;
			this.goTo(this.currentIndex);//stay in current index when flipping screen
		}
		
		var lastLI = totalLI - 1;
		//apply styles to each li
		for(i=0; i < totalLI; i++)
		{
			this.li[i].style.width = rspLiWidth;//taking 2px away because of borders
			this.li[i].style.clear = 'none';
			if (ipad){
				if (i !=  lastLI){
					this.li[i].style.marginRight = liMargin + 'px';
				}else{
					this.li[i].style.marginRight = 0 + 'px';
				}
			}else{
				this.li[i].style.marginRight = 0;
			}
		}
		//end for
		
		/*console.log('rspLiWidth: ' + rspLiWidth + 
					' this.slideAmmount: ' + this.slideAmmount +
					' liMargin: ' + liMargin + 
					' this.slideUnit: ' + this.slideUnit + 
					' this.ul.style.width: ' + this.ul.style.width + 
					' rspLiWidth: ' + rspLiWidth + 
					' this.clickCealing: ' + this.clickCealing + 
					' rspLiWidth: ' + rspLiWidth);*/
		//return;
		//console.log(document.body.clientWidth + ' window.innerWidth: ' + window.innerWidth);
	},
	resetUL: function(){
		$(this.ul).removeAttr('style');
		for(i=0; i < this.li.length; i++)
		{
			$(this.li[i]).removeAttr('style');
		}
	}
}


function RespondObj(sliderContext,liMargin,liToShow,totalLI,slideWindow, borderSize) {
	//multiply by liMargin by 2 because we only need two margins to show
	//take away 2 pixels for css borders
	this.rspLiWidth = Math.floor( (sliderContext - ((slideWindow-1) * liMargin) - ((borderSize * 2) * slideWindow)) / liToShow) ;
	//for sliding ammount purposes: adding the width of card plus margin we can move 1 at a time
	this.slideAmmount = this.rspLiWidth + liMargin + (borderSize * 2);
	this.slideUnit  = 'px';
	//width of container UL slider
	this.ulWidth = ((this.rspLiWidth + liMargin + borderSize) * totalLI) - liMargin + 'px';
	this.rspLiWidthAndUnit = this.rspLiWidth + 'px';
	//set a max for ipad
	this.clickCealing = totalLI - slideWindow;
}
	
function checkMediaQuery(mq)
{
	var mediaQuery = window.matchMedia(mq)
	if ( mediaQuery.matches )
		return true;
	else
		return false;
}
/*
	ele = html element
	prop = css property that you are after
	returns the css value but checks if the last two characters are 'px'
	if they are, they get removed so we can have a numeric value
*/
function getCSSprop(ele, prop)
{
	var value = ele.css(prop);
	if ( value.slice(-2) == 'px' )
		return value.slice(0,-2);
	else
		return value;
}

	

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
