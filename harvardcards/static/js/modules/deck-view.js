define([
	'jquery',
	'components/slider/DeckSlider', 
	'components/InlineEditor', 
	'components/FlipMode',
	'models/Deck', 
	'views/CardForm', 
	'utils/utils'
], function(
	$, 
	DeckSlider, 
	InlineEditor, 
	FlipMode,
	Deck, 
	CardForm, 
	utils
) {

function initModule() {
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
    var _currentCardID = null;
    var _direction = null;

	card_counter.update = $.proxy(card_counter.update, card_counter);

	deck_slider.bind("beforeslide", function(slider, card_id, next_card_id) {
        _direction = ( card_id > next_card_id ) ? "right" : "left";
		$cardDetail.find("[data-card-id]").hide("slide", { direction: _direction }, 1000);
        _currentCardID = card_id;
	});
	deck_slider.bind("slide", function(slider, card_id) {
        _direction = ( _currentCardID > card_id ) ? "left" : "right";
		$cardDetail.find("[data-card-id="+card_id+"]").show("slide", { direction: _direction }, 2000);
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
		MODULE.revealCard($(this), $(this).parent().next());
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
	this.setupFlipMode();
	this.setupEditableDeckTitle();
	this.setupKeyboardShortcuts();
};

	var MODULE = {
		initModule:initModule,
		// This function initializes flip mode
		setupFlipMode: function() {
			var flipMode = new FlipMode();
			return flipMode;
		},
		// This function adds the ability to inline edit elements with data-editable=yes.
		//
		// Assumes the element also has these data attributes:
		//		- data-editable-url: API endpoint URL
		//		- data-editable-field: name of the field to POST
		setupEditableDeckTitle: function() {
			$("[data-editable]").each(function(index, el) {
				var $el = $(el);
				var editable = $el.data('editable') || 'no';
				var deck_id = $el.data('editable-id') || '';
				if(editable !== 'yes') {
					return;
				}

				var editor = new InlineEditor($el, {
					edit: function(editor, value, settings) {
						var deck = new Deck({ id: deck_id });
						var result = deck.rename(value);
						editor.value = value;
						return result;
					},
					success: function(data, textStatus, xhr) {
						var success = data.success;
						var value = editor.value;
						if(success === true) {
							this.highlight({color: 'yellow'});
							$("#navigation").find("[data-deck-id='"+deck_id+"']").text(value);
						} else if(success === false) {
							this.highlight({color: 'false'});
						}
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
		},
		setupKeyboardShortcuts: function() {
			$(document).on('keydown', function(e) {
				MODULE.onKeyDownRevealCard(e.keyCode, function(state) {
					$button_el = $('#allCards > li.show .reveal');
					$reveal_content_el = $button_el.parent().next();
					MODULE.revealCard($button_el, $reveal_content_el, state);
				});
			});
		},
		onKeyDownRevealCard: function(keyCode, callback) {
			// reveal content when down arrow is pressed
			if(keyCode == 40) {
				callback(true);
			} else if(keyCode == 38) {
				callback(false);
			}
		},
		revealCard: function(buttonEl, revealContentEl, state) {
			var $button_el = $(buttonEl);
			var $reveal_content_el = $(revealContentEl);
			var button_text = ['Reveal', 'Hide'];
			var css_cls = ['show', 'hide'];

			// if no state is explicitly passed (true=reveal, false=hide), 
			// then assume we want to toggle the card
			if(typeof state === 'undefined') {
				state = !$reveal_content_el.hasClass('show');
			} else {
				state = !!state; // force boolean
			}

			if(state) {
				css_cls.reverse();
				button_text.reverse();
			}

			$reveal_content_el.removeClass(css_cls[0]).addClass(css_cls[1]);
			$button_el.text(button_text[0]);

			return state;
		}
	};

	return MODULE;
});
