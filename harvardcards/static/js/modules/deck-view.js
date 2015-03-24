define([
	'jquery',
	'components/slider/DeckSlider', 
	'components/InlineEditor', 
	'components/FlipMode',
	'models/API', 
	'models/Analytics', 
	'models/Deck', 
	'views/CardForm', 
	'utils/utils',
    'swiper'
], function(
	$, 
	DeckSlider, 
	InlineEditor, 
	FlipMode,
	API,
	Analytics,
	Deck, 
	CardForm, 
	utils,
    Swiper
) {

function initModule() {
	Analytics.run();

	var deck_slider = new DeckSlider($(".slider").first());
	var card_counter = {
		el: $("#counter"),
		slider: deck_slider,
		update: function() {
			var current = this.slider.getCurrentCardIndex();
			var total = this.slider.getNumItems();
			this.el.html(current + " / " + total);
		}
	};
	var $cardDetail = $("#singleCardHolder");

	card_counter.update = $.proxy(card_counter.update, card_counter);

	deck_slider.bind("beforeslide", function(slider, data){
		var $controls = $cardDetail.find(".controls[data-card-id]");
		var $card = $cardDetail.find(".card[data-card-id]");

		$controls.removeClass("card-active").hide();
		//$card.removeClass('card-active').hide();

		deck_slider._slideDirection = (data.toIndex >= data.fromIndex ? "right" : "left");
		deck_slider._slideCurrent = (data.toIndex == data.fromIndex);
	});

    deck_slider.bind("slide", function(slider, data) {
		var card_id = data.card_id;
		var $controls = $cardDetail.find(".controls[data-card-id="+card_id+"]");
		var $card = $cardDetail.find(".card[data-card-id="+card_id+"]");
		var playAudio = MODULE.makeAudioPlayer($card);
		var mode = $card.data("mode");

		var slideOpts = {
			direction: deck_slider._slideDirection,
			complete: playAudio
		};

        // send tracking
		Analytics.trackCard(card_id, mode);

		// show the card controls
		$controls.addClass('card-active');
		$controls.show();

		// show the card
		$card.addClass('card-active');


        if(deck_slider._slideCurrent) {
			$card.show();
			playAudio();
		}

    });

    /* Swiper */
    var mySwiper = new Swiper ('.swiper-container', {
        // Optional parameters
        direction: 'horizontal',
        nextButton: '.swiper-btn-next',
        prevButton: '.swiper-btn-prev',
        keyboardControl: true,
        loop: false,
        onSlideChangeStart: function(swiper){
            deck_slider.selectCard($(swiper.slides[swiper.activeIndex]).data('card-id'));
        	card_counter.update();

        }
    });
    $('.card-image').click(function(event){
        mySwiper.slideTo(deck_slider.getIndexOfCard($(event.currentTarget).data('card-id')));
    });
    $('#first_card').click(function(event){
        mySwiper.slideTo(0);
    });
    $('#last_card').click(function(event){
        mySwiper.slideTo(mySwiper.slides.length - 1);
    });
    var shuffleSwiper = function(card_ids){
        var slides = mySwiper.slides;
        mySwiper.removeAllSlides();
        for(var i = 0; i < card_ids.length; i++){
            for(var j = 0; j < slides.length; j++){
                card_id = $(slides[j]).data('card-id');
                if(card_ids[i] == card_id){
                    mySwiper.appendSlide(slides[j]);
                    break;
                }

            }
        }


    };
    /* End Swiper */

	deck_slider.bind("load", function(slider, card_ids) {
		MODULE.loadCardMedia(card_ids);
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
	    var shuffleText = 'Shuffle';
	    var resetText = 'Reset';

		if ($("#shuffle_cards .control-text").text() == shuffleText){
			deck_slider.shuffle();
            shuffleSwiper(deck_slider.card_ids);
			deck_slider.goToFirst();
			$("#shuffle_cards .control-text").text(resetText);
			$("#shuffle").removeClass('fa-random').addClass('fa-refresh');

		} else {
			deck_slider.reset();
            shuffleSwiper(deck_slider.card_ids);
			deck_slider.goToFirst();
			$("#shuffle_cards .control-text").text(shuffleText);
			$("#shuffle").removeClass('fa-refresh').addClass('fa-random');
		}
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

	// fixes the reorganization of slider
	$("#initDeck").css("display","none");
	$("#holder").css("display","block");
};

	var MODULE = {
		initModule:initModule,
		// This function initializes flip mode
		setupFlipMode: function() {
			var flipMode = new FlipMode({btnEl: "#flip_mode"});
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
							$("#navigation, .breadcrumbs").find("[data-deck-id='"+deck_id+"']").text(value);
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
					$button_el = $('#allCards > .card-active .reveal');
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
		},
		loadCardMedia: function(card_ids) {
			var loadedCls = 'cardFieldMediaLoaded';
			var loadMedia = {
				'A': function(data) {
					var html = '<audio alt="'+data.label+'" controls="controls" class="cardFieldAudio" preload="auto"><source src="'+data.src+'" />Your browser does not support the <code>audio</code> element.</audio>';
					return html;
				},
				'V': function(data) {
					var html = '<video alt="'+data.label+'" src="'+data.src+'" class="cardFieldVideo" controls>Your browser does not support the <code>video</code> element.</video>';
					return html;
				},
				'I': function(data) {
					var html = '<img src="'+data.src+'" alt="'+data.label+'" class="cardFieldImage" />';
					return html;
				}
			};
			$.each(card_ids, function(idx, card_id) {
				$('.card[data-card-id="'+card_id+'"] .cardFieldMedia').filter(function() {
					return !$(this).hasClass(loadedCls);
				}).each(function(idx, el) {
					var type = $(el).data("type");
					var params = {
						"src": $(el).data("src"),
						"label": $(el).data("label")
					};
					var result = loadMedia[type](params);
					$(el).addClass(loadedCls).append(result);
				});
			});
		},
		// Pauses all audio on the page.
		pauseAllAudio: function($allAudio) {
			$allAudio.each(function(idx, el) {
				this.pause();
			});
		},
		// Returns a function that will play the first audio file on the flashcard.
		makeAudioPlayer: function($card) {
			var $audio = $card.find("audio").first(); 
			var audio = ($audio.length == 1 ? $audio[0] : false);
			return function() {
				//console.log("play audio", $card.data('card-id'));
				MODULE.pauseAllAudio($('audio'));
				if(audio) {
					audio.load(); // have to re-load audio each time for safari/chrome 
					audio.play();
				}
			};
		}
	};

	return MODULE;
});
