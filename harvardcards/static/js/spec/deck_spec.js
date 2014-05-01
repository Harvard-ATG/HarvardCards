define(['lodash', 'jquery', 'models/Deck', function(_, $, Deck) {
	describe("Deck", function() {
		it("creates an empty instance", function() {
			var deck = new Deck();
			expect(deck.id).toBeNull();
			expect(deck.title).toBe('');
		});
		it("creates a non-empty instance", function() {
			var id = 123;
			var title = 'foo';
			var deck = new Deck({ id: id, title: title });
			expect(deck.id).toBe(id);
			expect(deck.title).toBe(title);
		});
		it("renames itself", function() {
			var new_title = "bar";
			var deck = new Deck({ id: 1, title: "foo" });
			var deferred;

			spyOn(deck, 'rename');
			deferred = deck.rename(new_title);

			expect(deck.rename).toHaveBeenCalled();
			expect(deck.rename).toHaveBeenCalledWith(new_title);
		});
	});
});
