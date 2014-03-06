define(['jquery', 'views/Slider'], function($, Slider) {
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
	
	
/*************************************************************************
					TOUCH EVENTS FOR DASHBAORD (START)
*************************************************************************/

	if (typeof(window.ontouchstart) != 'undefined' || typeof(window.onmspointerdown) != 'undefined')
	{
		$('.sliderNav').hide();
		
	}
	
	var TRANSITION     = 'transition',
        TRANSFORM      = 'transform',
        TRANSITION_END = 'transitionend',
        TRANSFORM_CSS  = 'transform',
        TRANSITION_CSS = 'transition';
            
    if (typeof document.body.style.webkitTransform !== undefined)
    {
        TRANSITION = 'webkitTransition';
        TRANSFORM = 'webkitTransform';
        TRANSITION_END = 'webkitTransitionEnd';
        TRANSFORM_CSS = '-webkit-transform';
        TRANSITION_CSS = '-webkit-transition';
    }
	
	function cleanTransitions(node)
	{
            node.style[TRANSITION] = 'none';
    }
    
	function attachTouchEvents()
	{
		var bd = document.querySelectorAll('.slider');
		var bdLength = bd.length;
		for ( i = 0; i < bdLength; i++ )
		{
			bd[i].addEventListener('touchmove', handleTouchEvents);
			bd[i].addEventListener('touchstart', handleTouchEvents);
			bd[i].addEventListener('touchend', handleTouchEvents);
		}
	}
		
	function setPosition(node, left) 
	{
        node.style[TRANSFORM] =  "translate3d("+left+"px, 0, 0)";
    }
                
	
    var startPos, lastPos, startPosY, lastPosY;
    
	function handleTouchEvents(e)
	{
		var direction = 0;
		
		var i = $(this).parent().index();
		if (e.type == 'touchstart')
		{
			startPos = e.touches[0].clientX;
			lastPos = startPos;
			direction = 0;
			
			startPosY = e.touches[0].clientY;
			lastPosY = startPosY;
		}
		else if (e.type == 'touchmove')
		{
			e.preventDefault();
			
			if (lastPos > startPos)
			{
				direction = -1;
			}
			else
			{
				direction = 1;
			}
			
			lastPosY = e.touches[0].clientY;
			lastPos = e.touches[0].clientX;
			
		}
		else if (e.type == 'touchend')
		{	
            if(lastPosY - startPosY > 50)
			{
				if ( $(this).parent().prev().hasClass('addCourseWrapper') )
				{
					//first slider scroll to top of page
            		$('html body').animate({scrollTop: $('html').position().top}, 500);
				}
				else
				{
					//page up
					$('html body').animate({scrollTop: $(this).parent().prev().position().top}, 500);
				}
            }
            else if (lastPosY - startPosY < -50)
            {
            	if ( !($(this).parent().prev().hasClass('courseWrapper')) )
            	{
            		//first slider scroll to top of page
            		$('html body').animate({scrollTop: $('html').position().bottom}, 500);
            	}
            	else
            	{
	            	//page down
	            	$('html body').animate({scrollTop: $(this).parent().next().position().top}, 500);
            	}
            }
            else
            {
	            if(lastPos - startPos > 100)
				{
	                sliders.decks[i-1].goToPrev();
	            }
	            else if (lastPos - startPos < -100)
	            {
	                sliders.decks[i-1].goToNext();
	            }
            }
		}	
	}
	
	attachTouchEvents();

/*************************************************************************
					TOUCH EVENTS FOR DASHBAORD (END)
*************************************************************************/
	
	window.sliders = sliders;

	return {initModule: function(){}};
});
