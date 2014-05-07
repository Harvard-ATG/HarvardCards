define(['jquery','components/slider/DeckSlider', 'components/InlineEditor', 'models/Deck', 'views/CardForm', 'utils/utils'], function($, DeckSlider, InlineEditor, Deck, CardForm, utils) {

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
	var $cardDetail = $("#singleCardHolder");

	card_counter.update = $.proxy(card_counter.update, card_counter);

	deck_slider.bind("beforeslide", function(slider, card_id) {
		$cardDetail.find("[data-card-id]").removeClass("show").addClass("hide");
	});
	deck_slider.bind("slide", function(slider, card_id) {
		$cardDetail.find("[data-card-id="+card_id+"]").removeClass("hide").addClass("show");
	});
	deck_slider.bind("slide", card_counter.update);
	deck_slider.goToCurrent();
	card_counter.update();

	$('#review_mode').click(function(){
	    location.href=this.href+'?card_id='+deck_slider.getCurrentCardId();
	    return false;
	});
	$('#quiz_mode').click(function(){
	    location.href=this.href+'&card_id='+deck_slider.getCurrentCardId();
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

	utils.setupConfirm();

	setupEditableDeckTitle();
};

// Add ability to edit inline every element with data-editable=yes.
// Note: also requires data-editable-url (API endpoint)
// and data-editable-field (name of the field to POST to the API)
function setupEditableDeckTitle() {
	$("[data-editable]").each(function(index, el) {
		var $el = $(el);
		var editable = $el.data('editable') || 'no';
		var id = $el.data('editable-id') || '';
		if(editable !== 'yes') {
			return;
		}

		var editor = new InlineEditor($el, {
			edit: function(editor, value, settings) {
				var deck = new Deck({ id: id });
				return deck.rename(value);
			},
			success: function(data, textStatus, xhr) {
				var success = data.success;
				if(!success) {
					window.alert("Error saving: "+ data.errors[field]);
				}
				return success;
			},
			error: function(xhr, textStatus, errorThrown) {
				window.alert("Error saving: "+ errorThrown);
			}
		});
	});
}

	return {initModule:initModule};
});
