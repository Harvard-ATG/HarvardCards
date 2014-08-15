define(['lodash', 'jquery', 'components/FlipMode'], function(_, $, FlipMode) {


	describe("Flip Mode", function() {

		beforeEach(function(){
			localStorage.removeItem('flip_mode');
			$('body').append('<div id="flip_fixture"><button id="flip_mode"></button><ul id="allCards"><li><div class="show_content"></div><div class="reveal_content"/></li></ul></div>');
		});
	
		afterEach(function(){
			$('#flip_fixture').remove();
		});

		it("button clickable", function(){
			var flipMode = new FlipMode;

			spyOn(flipMode, 'flipButton');
			$('#flip_mode').click();
			expect(flipMode.flipButton).toHaveBeenCalled();
			
		});

		it("button flips content", function(){
			var flipMode = new FlipMode;

			spyOn(flipMode, 'flipContent');
			$('#flip_mode').click();
			expect(flipMode.flipContent).toHaveBeenCalled();
			
		});
		
		it("flip button depresses", function(){
			var flipMode = new FlipMode;

			expect($('#flip_mode')[0].className.split(/\s+/)).not.toContain('down');
			$('#flip_mode').click();
			expect($('#flip_mode')[0].className.split(/\s+/)).toContain('down');
		});

		it("flip button aria-pressed", function(){
			var flipMode = new FlipMode;
			
			expect($('#flip_mode').attr('aria-pressed')).not.toBeDefined();
			$('#flip_mode').click();
			expect($('#flip_mode').attr('aria-pressed')).toBe('true');
		});


		it("flip localStorage", function() {
			var flipMode = new FlipMode;
			
			expect(localStorage['flip_mode']).not.toBeDefined();
			$('#flip_mode').click();
			expect(localStorage['flip_mode']).toBe('true');
		});
		
		it("flip content", function(){
			var flipMode = new FlipMode;
			
			$('.show_content').html('asdf');
			var show = $('.show_content').html();
			$('.reveal_content').html('jkl;');
			var reveal = $('.reveal_content').html();
			
			expect($('.show_content').html()).toBe(show);
			expect($('.reveal_content').html()).toBe(reveal);
			
			$('#flip_mode').click();
			
			expect($('.show_content').html()).toBe(reveal);
			expect($('.reveal_content').html()).toBe(show);
		});

	});
});
