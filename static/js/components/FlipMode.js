define(['jquery'], function($) {

	/**
	 * FlipMode object supports flip mode on flashcard decks.
	 */
	var FlipMode = function(config) {
		this.config = config || {};
		this.onClick = $.proxy(this.onClick, this);
		this.localStorage = localStorage;
		this.storeKey = 'flip_mode';
		this.flipped = false;
		this.init();
	};

	FlipMode.prototype.init = function() {
		this.flipButton(this.isFlipModeOn());
		$(this.config.btnEl).click(this.onClick); 
	};

	FlipMode.prototype.onClick = function(e) {
		this.flipButton(!this.isFlipModeOn());
	};

	FlipMode.prototype.setFlipMode = function(flipped) {
		if(flipped) {
			this.localStorage[this.storeKey] = true;
		} else {
			this.localStorage.removeItem(this.storeKey);
		}
	};

	FlipMode.prototype.isFlipModeOn = function() {
		return this.localStorage[this.storeKey] || false;
	};
	
	FlipMode.prototype.flipButton = function(pressed){
		var btnEl = this.config.btnEl;
		if(pressed){
			$(btnEl).addClass('down').attr('aria-pressed', 'true');
		} else {
			$(btnEl).removeClass('down').attr('aria-pressed', 'false');
		}
		this.setFlipMode(pressed);
		this.flipContent(pressed);
	};
	
	FlipMode.prototype.flipContent = function(flip){
		if(flip == this.flipped) {
			return;
		}
		$('#allCards .card[data-card-id]').each(function(idx, item){
			var showed = $(this).find('.show_content').html();
			var revealed = $(this).find('.reveal_content').html();
			$(this).find('.show_content').html(revealed);
			$(this).find('.reveal_content').html(showed);
		});
		this.flipped = !this.flipped;
	};

	return FlipMode;
});
