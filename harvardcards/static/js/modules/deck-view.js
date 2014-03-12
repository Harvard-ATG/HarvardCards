define(['jquery', 'views/Slider', 'views/CardForm', 'jquery.appendAround', 'jqueryui', 'jquery.mousewheel'], function($, Slider, CardForm) {

// http://www.quirksmode.org/dom/domform.html

function moreFields() {
	counter++;
	var newFields = document.getElementById('readroot').cloneNode(true);
	newFields.id = '';
	newFields.style.display = 'block';
	var newField = newFields.childNodes;
	for (var i=0;i<newField.length;i++) {
		var theName = newField[i].name
		if (theName)
			newField[i].name = theName + counter;
	}
	var insertHere = document.getElementById('writeroot');
	insertHere.parentNode.insertBefore(newFields,insertHere);
	$('.moreField').each(function(){
        $(this).bind('click',function(){
            console.log(this.parentNode);
            this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode);
            counter=counter-1;
            return false;
        })
	})
}



$(document).ready(function(){
    //moreFields();
    $('#cards').children().each(
        function(){
            $(this).bind('click',function(){
                current = Number($(this).attr('id'));
                sliders[0].goToCard(current);
                return false;
            })
        });

    $('#reviewM').click(function(){
        location.href=this.href+'?cardLoc='+(current+1);
        return false;
    });
    $('#quizM').click(function(){
        location.href=this.href+'&cardLoc='+(current+1);
        return false;
    });
   $('#moreFields').click(function(){
        moreFields();
        return false;
    });





});

$('#addCard').click(function(){
    $('#cardFormContainer').toggle();
    $('#singleCardHolder').toggle();
    return false;
});

$('#card_cancel').click(function(){
    $('#cardFormContainer').hide();
    $('#singleCardHolder').show();
    return false;
});

function extractDeckId(){
    var pathname = $(location).attr('href');
    var res = String(pathname.match('[^/]+$'));
    res = res.match('([0-9]+).*');
    res = res.slice(1);
    return res;
};

$('#card_create').click(function(){
        $("#deck_id").val(extractDeckId());
        $('#cardForm').submit();
        return false;
});



// stackoverflow
function parseURLParams(url) {
    var queryStart = url.indexOf("?") + 1,
        queryEnd   = url.indexOf("#") + 1 || url.length + 1,
        query = url.slice(queryStart, queryEnd - 1),
        pairs = query.replace(/\+/g, " ").split("&"),
        parms = {}, i, n, v, nv;

    if (query === url || query === "") {
        return;
    }

    for (i = 0; i < pairs.length; i++) {
        nv = pairs[i].split("=");
        n = decodeURIComponent(nv[0]);
        v = decodeURIComponent(nv[1]);

        if (!parms.hasOwnProperty(n)) {
            parms[n] = [];
        }

        parms[n].push(nv.length === 2 ? v : null);
    }
    return parms;
}
sliders = [];
sliderLength = $('ul#cards li').size();
var pathname = $(location).attr('href');
var urlPar = parseURLParams(pathname);
current = 0;
if(typeof(urlPar) != "undefined"){
    if(typeof(urlPar["cardLoc"]) != "undefined"){
        var k = Number(urlPar["cardLoc"][0])-1;
        if (k>=0 && k<=sliderLength-1){
            current=k;
        }
    }
}
sliders = [];
fullCardSlider = [];
sliderLength = $('ul#cards li').size();

/*
$( "#slider" ).slider({
        orientation: "horizontal",
        min: 0,
        range: "min",
        max: sliderLength-1,
        step: 1,
        slide:function(event, ui){sliders[0].goToCard(ui.value)}
});

*/
var sliderObjExist = false;
var Slider1 = Slider;
$('.cardHolder').each(function() {
	if ( $(this).text() != '' ){
		//create Slider objects
		sliders.push(new Slider1(this,true,false));
		//sliders[i].respond();
		sliderObjExist = true;
	}
});


$('.test').each(function() {
	if ( $(this).text() != '' ){
		//create Slider objects
		fullCardSlider.push(new Slider1(this,true,true));
		//sliders[i].respond();
		sliderObjExist = true;
	}
});

sliders[0].goToCard(current);
// fixes the reorganization of slider
$("#initDeck").css("display","none");

$("#holder").css("display","block");

function updateCardLoc(loc){
    numCards = sliderLength;
	var location = Math.round((loc+1)/sliderLength*100) + '%  •  Card '+ (loc + 1) + ' of ' + sliderLength;
	$('#cardLoc').text(location);
	$( "#slider" ).slider( "value", loc );
}


$(window).on("resize", function () {
    // to display the card location between the control buttons
    spaceBtwControls = $('#controlbar').width()- $('#first').width()-$('#last').width()-$('#next').width()-$('#previous').width();
    $('#cardIndex').width(spaceBtwControls + 'px');

	if ( sliderObjExist )
	{
		//console.log($('.sliderNav').css('display'));
		sliders[0].respond();

	}
/* //RM
	var cardHolder = $('#singleCardHolder');
	var holderWidth = Math.round(cardHolder.width());
	var cardItems = $('#singleCardHolder ul li');
	var liCount = cardItems.length;
	//give each a card li the width of the container
	cardItems.width(holderWidth + 'px');
	//make the ul width big enough to fit all cards side by side
	var ulWidth = holderWidth * liCount;
	$('#singleCardHolder ul').width(ulWidth + 'px');

	//on first load show the first card
	cardItems.eq(current).show();
	sliders[0].goTo(current);

    updateCardLoc(current);
	document.getElementById(current).className = "clicked"
*/
	//change main card based on thumbnail click
	/*$('a.image').click(function(){
		var i = $(this).parent().index();

		if (i != current)
		{
			cardItems.eq(current).hide();
			document.getElementById(current).className = "";
            sliders[0].changeView(i);
			cardItems.eq(i).show();

			updateCardLoc(i);
			document.getElementById(i).className = "clicked"
			current = i;
		}
        else if (i===0 || i===sliderLength-1)
            sliders[0].goTo(i)

	});*/


}).resize();


/* accessibility (start) */
$('body').attr('role', 'application');

/* get the id of the key been pressed */
var getElementId = function($){
	return $.attr("id");
}

$('a').keydown(function(event){
	
	//console.log(event.keyCode);
	switch(event.keyCode)
	{
		case 9: //tab key
			//console.log($(this).attr('id'));
		break;
		case 13://enter key
			//$('#content').attr({ "role":"widget", "tabindex": "0" });
			//console.log(getLinkId($(this)));
			/*if (getElementId($this) == 'prevCard')
			{
				sliders[0].goToPrev();
			}
			else if (getLinkId($this) == 'firstCard')
			{
				sliders[0].goToFirstCard();
			}*/
		break;
	}
	
});
/* accessibility (end) */


$('.reveal').click(function() {
	var $show = $(this).parent().next();
	if ($show.hasClass('show')){
		$show.removeClass('show');
		$show.addClass('hide');
		$(this).text('Reveal');
	}else{
		$show.removeClass('hide');
		$show.addClass('show');
		$(this).text('Hide');
	}
	return false;
});


$('#full_screen').click(function() {
    var txt1 = 'Full Screen';
    var txt2 = 'Exit Full Screen';
    if ($("#full_screen").text() == txt1){
        $("#wrapper").children().not("#singleCardHolder").hide();
        $("#navigation").hide();
        $("#appTitle").hide();
        $("#singleCardHolder").css('margin-left','8.5%');
        $("#full_screen .control-text").text(txt2);
		$("#full").addClass("fa-compress").removeClass("fa-expand");
    }
    else{
        $("#wrapper").children().not("#cardFormContainer").show();
        $("#navigation").show();
        $("#appTitle").show();
        $("#singleCardHolder").css('margin-left','0');
        $("#full_screen .control-text").text(txt1);
		$("#full").addClass("fa-expand").removeClass("fa-compress");
    }
    return false;
});

// http://standardofnorms.wordpress.com/2012/04/08/shuffling-all-the-children-of-a-parent-element-in-javascript/
$('#shuffle_cards').click(function() {
    var cards  = $('#cards');
    var child = cards.children();
    while (child.length) {
        cards.append(child.splice(Math.floor(Math.random() *  child.length), 1));
    }
    return false;
});


$('#play_cards').click(function(){
    var txt1 = 'Play';
    var txt2 = 'Pause';
    if ($("#play_cards .control-text").text() == txt1){
        myintrval = setInterval(function(){
            if (current >= sliderLength-1)
                $('#play_cards').click();
            $('#next_card').click();
        }, 5000);
        $("#play_cards .control-text").text(txt2);
		$("#play").removeClass('fa-play').addClass('fa-pause');
    }
    else{
        clearInterval(myintrval);
        $("#play_cards .control-text").text(txt1);
		$("#play").removeClass('fa-pause').addClass('fa-play');
    }
    return false;
});

$('#previous_card').click(function() {
    if (current != 0){current = current - 1}
    sliders[0].goToPrev();
    return false;
});
$('#next_card').click(function() {
    if (current != sliderLength - 1){current = current + 1}
    sliders[0].goToNext();
    return false;
});

$('#first_card').click(function() {
    sliders[0].goToFirst();
    current = 0;
    return false;
});

$('#last_card').click(function() {
    sliders[0].goToLast();
    current = sliderLength - 1;
    return false;
});
// scroll through the slider using horizontal mousewheel/touchpad

$('#cardSlider').mousewheel(function(event) {
      if (event.deltaX>0){
        event.preventDefault();
        $('#next_card').click();
      }
      else if (event.deltaX<0){
      	event.preventDefault();
        $('#previous_card').click();
      }
});

function checkKey(e) {
    var event = window.event ? window.event : e;
    if (true) {
        if (event.keyCode == 37)
            $('#previous_card').click();
            //sliders[0].goToPrev()
        if (event.keyCode == 39)
            $('#next_card').click();
            //sliders[0].goToNext()    
    }
};
document.onkeydown=checkKey;

$(document).ready(function() {
	var card_form = new CardForm({
		formEl: "#cardForm",
		formMessageEl: "#cardForm .formMessage"
	});
	card_form.init();
});

	return { initModule: function() {} };
});
