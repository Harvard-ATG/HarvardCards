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
		
		this.respond();
		
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
		var ulwidth, rspLiWidth, liMargin, ipad, liToShow, borderAmmount;
		//border width of scroller li
		if (this.deckView)
			borderAmmount = 12;
		else
			borderAmmount = 2;
			
		var sliderContext = $(this.ul).parent().width();
		//total list item
		var totalLI = this.li.length;
		//li's borders to get added to the ul width
		var liBorders = borderAmmount * totalLI;
		//li margin only to be use with ipad
		liMargin = 30;
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
			this.goTo(0);//reset index
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
	
	

 
// JavaScript Document
$(document).ready(function(e) {
    
	$('a.arrowExpand').click(function() {
	   var ulDeckMenu = $(this).next();
	   //console.log(ulDeckMenu);
	   $(ulDeckMenu).toggle();
	   $(this).hide();
	   //adds the class that positions the open deck menu
	   //inside the deck
	   $(ulDeckMenu).addClass('openDeckMenu');
	   return false;
	});
 
 	$('a.arrowCollapse').click(function() {
	   var ulDeckMenu = $(this).parent().parent();
	   //console.log(ulDeckMenu);
	   $(ulDeckMenu).toggle();
	   $(this).parent().parent().parent().find('a.arrowExpand').show();
	   
	   //closes the admin menu by removing the css class
	   //that opens it
	   $(ulDeckMenu).removeClass('openDeckMenu');
	   return false;
	});
  	
	
	/*var sliders = [];
	var sliderObjExist = false;
	$(window).on("resize", function () {
		
		$('.slider').each(function() {
			if ( $(this).text() != '' ){
				//create Slider objects
				sliders.push(new Slider(this));
				sliderObjExist = true;
			}	
		});
		
		if ( sliderObjExist )
		{
			if ($('.noslider').text() != ''){
				//removing the size when going back into the noslider div
				sliders[0].resetUL();
			}else{
				sliders[0].respond();
			}
		}
	}).resize();*/
	
	
});

