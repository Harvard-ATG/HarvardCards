define(['jquery', 'modules/deck-view'], function($, DeckViewModule) {
	describe("DeckViewModule", function() {
		describe("revealCard", function() {
			it("toggles the reveal when state is explicitly passed", function() {
				var tests = [
					{state:true,text:'Hide',cls:'show'},
					{state:false,text:'Reveal',cls:'hide'}
				];
				_.each(tests, function(test) {
					var $button = $("<button/>");
					var $content = $("<div/>");
					var result = DeckViewModule.revealCard($button, $content, test.state);
					expect(result).toBe(test.state);
					expect($button.text()).toBe(test.text)
					expect($content.hasClass(test.cls)).toBe(true);
				});
			});
			it("toggles the reveal when no state is passed", function() {
				var tests = [
					{before_cls:'show',after_cls:'hide',state:false,text:'Reveal'},
					{before_cls:'hide',after_cls:'show',state:true,text:'Hide'}
				];
				_.each(tests, function(test) {
					var $button = $("<button/>");
					var $content = $('<div class="'+test.before_cls+'"/>');
					var result = DeckViewModule.revealCard($button, $content);
					expect(result).toBe(test.state);
					expect($button.text()).toBe(test.text);
					expect($content.hasClass(test.after_cls)).toBe(true);
				});
			});
		});
		describe("onKeyDownRevealCard", function() {
			it("executes callback with correct state when keyup or keydown is passed", function() {
				var tests = [
					{keyCode:40, state:true, callback: function() {}, valid: true},
					{keyCode:38, state:false, callback: function() {}, valid: true},
					{keyCode:39, state:false, callback: function() {}, valid: false}
				];
				_.each(tests, function(test) {
					spyOn(test, 'callback');
					DeckViewModule.onKeyDownRevealCard(test.keyCode, test.callback);
					if(test.valid) {
						expect(test.callback).toHaveBeenCalled();
						expect(test.callback).toHaveBeenCalledWith(test.state);
					} else {
						expect(test.callback).not.toHaveBeenCalled();
					}
				});
			});
		});
	});
});
