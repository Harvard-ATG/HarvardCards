define(['jquery'], function($) {
	describe("a test suite", function() {
		it("contains a spec", function() {
			var html = '<p>foo</p>';
			var $el = $('<div>').html(html);
			expect($el[0].innerHTML).toBe(html);
		});
	});
});
