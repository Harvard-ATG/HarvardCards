define(['jquery','components/slider/DeckSlider','views/CardForm'], function($,DeckSlider,CardForm) {

var deck_slider = new DeckSlider($("#holder"));

function updateCardCounter() {
	var current = deck_slider.getCurrentCardNum();
	var total = deck_slider.getNumItems();
	$("#counter").html(current + " / " + total);
};

updateCardCounter();

deck_slider.bind("slide", updateCardCounter);

deck_slider.bind("beforeslide", function(slider, card_id) {
	$("#allCards").find("[data-card-id]").removeClass("show").addClass("hide");
});
deck_slider.bind("slide", function(slider, card_id) {
	$("#allCards").find("[data-card-id="+card_id+"]").removeClass("hide").addClass("show");
});



$('#review_mode').click(function(){
    location.href=this.href+'?cardLoc='+deck_slider.getCurrentCardId();
    return false;
});
$('#quiz_mode').click(function(){
    location.href=this.href+'&cardLoc='+deck_slider.getCurrentCardId();
    return false;
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

$('#card_create').click(function(){
        $('#cardForm').submit();
        return false;
});







// fixes the reorganization of slider
$("#initDeck").css("display","none");
$("#holder").css("display","block");


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
	deck_slider.shuffle();
	deck_slider.goToFirst();
    return false;
});


$('#play_cards').click(function(){
    var txt1 = 'Play';
    var txt2 = 'Pause';
	var sliderLength = deck_slider.getNumItems();
    if ($("#play_cards .control-text").text() == txt1){
        myintrval = setInterval(function(){
            if (!deck_slider.goToNext()) {
                $('#play_cards').click();
            }
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

// Setup Slider Button Controls
$.each({
	"#first_card": "goToFirst",
	"#previous_card": "goToPrev",
	"#next_card": "goToNext",
	"#last_card": "goToLast",
	".mobileFirst": "goToFirst",
	".mobilePrevious": "goToPrev",
	".mobileNext": "goToNext",
	".mobileLast": "goToLast"
}, function(key, value) {
	$(key).on("click", function(evt) {
		evt.preventDefault();
		deck_slider[value]();
	});
});


var card_form = new CardForm({
	formEl: "#cardForm",
	formMessageEl: "#cardForm .formMessage"
});
card_form.init();


	return { initModule: function() {} };
});
