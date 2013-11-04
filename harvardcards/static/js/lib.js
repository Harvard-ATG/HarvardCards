var Slider = function() { this.initialize.apply(this, arguments) }
	Slider.prototype = {
	
		initialize: function(slider) {
		  this.ul = slider.children[0]
		  this.li = this.ul.children
		
		  // make <ul> as large as all <li>’s
		  this.ul.style.width = (this.li[0].clientWidth * this.li.length) + 'px'
		
		  this.currentIndex = 0
		},
		
		goTo: function(index) {
		  // filter invalid indices
		  if (index < 0 || index > this.li.length - 1)
			return
		
		  // move <ul> left
		  this.ul.style.left = '-' + (100 * index) + '%'
		
		  this.currentIndex = index
		},
		
		goToPrev: function() {
		  this.goTo(this.currentIndex - 1)
		},
		
		goToNext: function() {
		  this.goTo(this.currentIndex + 1)
		}
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
	});
 
 	$('a.arrowCollapse').click(function() {
	   var ulDeckMenu = $(this).parent().parent();
	   //console.log(ulDeckMenu);
	   $(ulDeckMenu).toggle();
	   $(this).parent().parent().parent().find('a.arrowExpand').show();
	   
	   //closes the admin menu by removing the css class
	   //that opens it
	   $(ulDeckMenu).removeClass('openDeckMenu');
	});
  	
	
	
});