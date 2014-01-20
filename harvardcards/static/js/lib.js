define(['jquery'], function($) {

var Slider = function() { this.initialize.apply(this, arguments) }

Slider.prototype = {

	initialize: function(slider,deckView) {
		//this.slider = slider;
		this.ul = slider.children[0]
		if (!this.ul){
			return;
		}

		this.li = this.ul.children
		this.currentIndex = 0
		//for ipad sliding, we want ot set a cealing for clicks
		//so it stops at the last li and not click onto empty space 
		if (deckView){
			this.deckView = true;
			this.liToShow = 4;
			this.slideWindow = 4;
		}else{
			this.liToShow = 3;
			this.slideWindow = 3;
		}
		
		this.totalLi = this.li.length;
		this.clickCealing;
		
		this.slideAmmount = 0;
		this.slideUnit = '%';
		this.border = 0;
		this.liMargin = 0;
		this.respond();
		
	},

	goTo: function(index) {
		// filter invalid indices

		if (index < 0 || index > this.li.length-1)
		return
		// move <ul> left
		//this.ul.style.left = '-' + (this.slideAmmount * index) + this.slideUnit;
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
		//console.log ('goTo: ' + this.currentIndex);
	},
	
	goToPrev: function() {
	    if (this.currentIndex == 2)
		    this.goTo(this.currentIndex - 2)
		else if (this.currentIndex == this.li.length-1)
		    this.goTo(this.currentIndex - 2)
        else
	    	this.goTo(this.currentIndex - 1)
		//console.log ('prev: ' + this.currentIndex);
	},
	changeView: function(i) {
        if (i <= 1)
            this.goTo(0);
        else
            this.goTo(i);
            //console.log ('prev: ' + this.currentIndex);
	},
	goToNext: function() {
	    if (this.currentIndex == 0)
	        this.goTo(this.currentIndex + 2)
	    else
		    this.goTo(this.currentIndex + 1)
		//console.log ('next: ' + this.currentIndex);
	},

	changeCard: function(num){
        current_card =$('li.clicked').attr('id');
        if (num === -1)
        {
            next_card =Number(current_card) - 1;
        }
        if (num === 1)
        {
            next_card = Number(current_card) + 1;
        }
        if (next_card >=0 && next_card < this.li.length){
            $(this.li[next_card].children).click();
        }
        else
            this.goTo(current_card);
	},

    firstCard: function(){
        var first_card = this.li[0];
        $(first_card.children).click();
    },
    goToCard: function(i){
        var card = this.li[i];
        $(card.children).click();
    },
    lastCard: function(){
        var last_card = this.li[this.li.length-1];
        $(last_card.children).click();
    },

	respond: function(){
		var ulwidth, rspLiWidth, liMargin, ipad, liToShow, borderAmmount;
		//border width of scroller li
		if (this.deckView)
			borderAmmount = 12;

		else
			borderAmmount = 2;
		this.border = borderAmmount;
		var sliderContext = $(this.ul).parent().width();
		//total list item
		var totalLI = this.li.length;
		//li's borders to get added to the ul width
		var liBorders = borderAmmount * totalLI;
		//li margin only to be use with ipad
		liMargin = 30;
		this.liMargin = liMargin;
		//li to show on ipad view
		liToShow = this.liToShow;
		
		var mq = window.matchMedia("(min-width: 768px) and (max-width: 1024px)");
		
		if (mq.matches || this.deckView)
		{
			var respUnits = new RespondObj(sliderContext,liMargin,liToShow,this.totalLi,this.slideWindow, borderAmmount);
			
			rspLiWidth = respUnits.rspLiWidthAndUnit;
			this.slideAmmount = respUnits.slideAmmount;
			this.slideUnit = respUnits.slideUnit;
			this.ul.style.width = respUnits.ulWidth;
			this.clickCealing = respUnits.clickCealing;
			
			ipad = true;
			this.goTo(this.currentIndex);//reset index
		}
		else
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
	this.rspLiWidth = Math.floor((sliderContext - (2*liMargin)) / liToShow) - borderSize;
	//for sliding ammount purposes: adding the width of card plus margin we can move 1 at a time
	this.slideAmmount = this.rspLiWidth + liMargin;
	this.slideUnit  = 'px';
	//width of container UL slider
	this.ulWidth = ((this.rspLiWidth + liMargin + borderSize) * totalLI) - liMargin + 'px';
	this.rspLiWidthAndUnit = this.rspLiWidth + 'px';
	//set a max for ipad
	this.clickCealing = totalLI - slideWindow;
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
