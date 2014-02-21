define(['jquery'], function($) {

var Slider = function() { this.initialize.apply(this, arguments) }
Slider.prototype = {

	initialize: function(slider,deckView,fullCard) {
		//to force scroller on view and review modes thumbnails
		//regardles of monitor size. Homepage or "dashboard" set to false
		if (typeof deckView === "undefined" || typeof fullCard === "undefined")
		{
			this.deckView = false;
			this.fullCard = false;
		}
		else
		{
			this.deckView = deckView;
			this.fullCard = fullCard;
		}
		
		this.ul = slider.children[0]
		if (!this.ul){
			return;
		}
		
		//set the li's
		this.li = this.ul.children
		//get the border width for the li's
		this.liborder = getCSSprop($(this.li),'border-left-width');
		
		this.currentIndex = 0;
		
		
		this.totalLi = this.li.length;
		this.clickCealing;
		
		this.slideAmmount = 0;
		this.slideUnit = '%';
		this.border = 0;
		this.liMargin = 0;
		
		//show the first card on load
		this.showCard(0);
		//give the first card an active class
		$(this.li).eq(0).addClass('cardActive');
		
	    this.respond();
	},
	
	goTo: function(index) {
		// filter invalid indices
		if (index < 0 || index > this.li.length - 1 )
		return
		
		// move <ul> left
		this.ul.style.left = '-' + (this.slideAmmount * index) + this.slideUnit;
		
		this.currentIndex = index;
		
		this.cardCounter();
		/*
        if (index == 0)
            this.ul.style.left = index + this.slideUnit;
        else if (index == this.li.length -1 || index == this.li.length -2)
        {
            fullWidth = (this.li.length-3)*(this.slideAmmount + this.border) - this.liMargin;
            addShift = fullWidth - this.liMargin - this.border/2 -  0.6*(this.slideAmmount -this.liMargin);
            this.ul.style.left = '-' + addShift+ this.slideUnit;
        }
        else
        {
	        var shiftBy = (this.slideAmmount+this.border) *(index-2) + 0.68*(this.slideAmmount - this.liMargin + this.border);
	    	this.ul.style.left = '-' + shiftBy + this.slideUnit;
        }
		this.currentIndex = index;
		*/
	},
	
	goToPrev: function() {
	    if ( this.deckView && this.currentIndex > 0 )
		{
			this.hideCard(this.currentIndex);
			this.showCard(this.currentIndex - 1);
		}
	    this.goTo(this.currentIndex - 1);
	    
	    /*
	    if (this.currentIndex == 2)
		    this.goTo(this.currentIndex - 2)
		else if (this.currentIndex == this.li.length-1)
		    this.goTo(this.currentIndex - 2)
        else
	    	this.goTo(this.currentIndex - 1)
		*/
	},
	/*changeView: function(i) {
        if (i <= 1)
            this.goTo(0);
        else
            this.goTo(i);
            //console.log ('prev: ' + this.currentIndex);
	},*/
	goToNext: function() {
		this.goTo(this.currentIndex + 1);
		
		if ( this.deckView )
		{
			this.hideCard(this.currentIndex - 1);
			this.showCard(this.currentIndex);
		}
	    
	},
	goToFirst: function(){
		this.hideCard(this.currentIndex);
		this.showCard(0);
		
		this.goTo(0);
	},
	goToLast: function(){
		
		this.hideCard(this.currentIndex);
		this.showCard(this.totalLi-1);
		
		this.goTo(this.totalLi-1);
	},
	
	showCard: function(index){
		//mark the current thumb as checked
		$(this.li).eq(index).addClass('cardActive');
		
		$('ul#allCards li').eq(index).removeClass('hide').addClass('show');
	},
	
	hideCard: function(index){
		$(this.li).eq(index).removeClass('cardActive');
		document.getElementById(index).children[0].blur();
		
		$('ul#allCards li').eq(index).removeClass('show').addClass('hide');
	},
	
	goToCard: function(card){
		this.hideCard(this.currentIndex);
		this.showCard(card);
		this.currentIndex = card;
		
		this.cardCounter();
	},
	
	cardCounter: function(){
		if ( this.deckView )
		{
		var counter = document.getElementById("counter");
		counter.innerHTML = (this.currentIndex + 1) + "/" + this.totalLi;
		}
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
		this.liMargin = liMargin;
		//li to show on ipad view
		//liToShow = this.liToShow;
		
		//var mq = window.matchMedia("(min-width: 768px) and (max-width: 1024px)");
		
		if ((twoCards || threeCards || fourCards || this.deckView) && !(this.fullCard)) //(mq.matches || this.deckView)
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
		else if ((oneCard || twoCards || threeCards || this.deckView) && (this.fullCard))
		{
			//give the UL a new width to accomodate all the li's plus their margins
			ulwidth = (sliderContext * totalLI);
			this.ul.style.width = ( ulwidth + liBorders ) + 'px';
			rspLiWidth = sliderContext-2 + 'px';//width of li
			//ammount to slide: in this 100 since ther is only one card
			this.slideAmmount = 100;
			this.slideUnit = '%';
			
			this.clickCealing = this.totalLi - 1;
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

/* 
	takes in mq = media query to be checked
	returns true/false
*/	
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
