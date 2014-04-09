define(['jquery','components/slider/DeckSlider','views/CardForm'], function($,DeckSlider,CardForm) {

var initModule = function() {
	var deck_slider = new DeckSlider($(".slider").first());
	var card_counter = {
		el: $("#counter"),
		slider: deck_slider,
		update: function() {
			var current = this.slider.getCurrentCardNum();
			var total = this.slider.getNumItems();
			this.el.html(current + " / " + total);
		}
	};
	card_counter.update = $.proxy(card_counter.update, card_counter);

	deck_slider.bind("beforeslide", function(slider, card_id) {
		$("#allCards").find("[data-card-id]").removeClass("show").addClass("hide");
	});
	deck_slider.bind("slide", function(slider, card_id) {
		$("#allCards").find("[data-card-id="+card_id+"]").removeClass("hide").addClass("show");
	});
	deck_slider.bind("slide", card_counter.update);
	deck_slider.goToFirst();
	card_counter.update();

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
	        $("#wrapper").children().not("#singleCardHolder, .fullcardBtns").hide();
	        $("#appTitle, #navigation").hide();
	        $("#singleCardHolder").css('margin-left','8.5%');
	        $("#full_screen .control-text").text(txt2);
			$("#full").addClass("fa-compress").removeClass("fa-expand");
	    }
	    else{
	        $("#wrapper").children().not("#cardFormContainer, .fullcardBtns").show();
			$("#appTitle, #navigation").show();
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
	    var playText = 'Play';
	    var pauseText = 'Pause';
	    if ($("#play_cards .control-text").text() == playText){
			deck_slider.play(function() {
				$("#play_cards").click();
			});
	        $("#play_cards .control-text").text(pauseText);
			$("#play").removeClass('fa-play').addClass('fa-pause');
	    }
	    else{
			deck_slider.pause();
	        $("#play_cards .control-text").text(playText);
			$("#play").removeClass('fa-pause').addClass('fa-play');
	    }
	    return false;
	});


	var card_form = new CardForm({
		formEl: "#cardForm",
		formMessageEl: "#cardForm .formMessage"
	});
	card_form.init();
};

	return {initModule:initModule};
});
