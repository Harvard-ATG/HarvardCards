define(['jquery'], function($) {

	/**
	 * 
	 */
	var FlipMode = function() {
		this.init();
	};

	FlipMode.prototype.init = function() {
		var that = this;
		if(localStorage.flip_mode){
			that.flipButton(true);
		}
		$('#flip_mode').click(function(){
			if(localStorage.flip_mode){
				that.flipButton(false);
			} else {
				that.flipButton(true);
			}
		});
	};
	
	FlipMode.prototype.flipButton = function(flipBool){
		var that = this;
		if(flipBool){
			$('#flip_mode').addClass('down');
			$('#flip_mode').attr('aria-pressed', 'true');
			localStorage['flip_mode'] = true;
			that.flipContent();
		} else {
			$('#flip_mode').removeClass('down');
			$('#flip_mode').attr('aria-pressed', 'false');
			localStorage.removeItem('flip_mode');
			that.flipContent();
		}
	}
	
	FlipMode.prototype.flipContent = function(){
		$('#allCards > li').each(function(item){
			var showed = $(this).find('.show_content').html();
			var revealed = $(this).find('.reveal_content').html();
			$(this).find('.show_content').html(revealed);
			$(this).find('.reveal_content').html(showed);
		});
	}

	return FlipMode;
});
