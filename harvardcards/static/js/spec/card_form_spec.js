define(['jquery', 'views/CardForm'], function($, CardForm) {
	var getFixture = function() {
		var htmlFixture = '<form method="post" action=""><div class="message"></div><input type="submit" name="submit" value="Submit" /></form>';
		return $('<div>').html(htmlFixture);
	};

	var getCardFormWithFixture = function() {
		var fixture = getFixture();
		var formEl = fixture;
		var formMessageEl = fixture.find('.message');
		var card_form = new CardForm({formEl: formEl, formMessageEl: formMessageEl});
		card_form.init();
		return card_form;
	};

	describe("CardForm", function() {
		it("throws error on invalid config", function() {
			var factory = function(config) {
				return function() {
					new CardForm(config);
				};
			};
			expect(factory()).toThrow();
			expect(factory({})).toThrow();
			expect(factory({formEl:'',formMessageEl:''})).toThrow();
			expect(factory({formEl:'.foo',formMessageEl:'.bar'})).not.toThrow();
		});

		it("constructs an object", function() {
			var card_form = getCardFormWithFixture();
			expect(card_form.formEl).toBeTruthy();
			expect(card_form.formMessageEl).toBeTruthy();
		});

		it("shows an info message before submitting", function() {
			var card_form = getCardFormWithFixture();
			spyOn(card_form, 'beforeSubmit');
			spyOn(card_form, 'message');
			card_form.formOpts.beforeSubmit().andCallThrough();
			expect(card_form.message).toHaveBeenCalled();
			expect(card_form.message.mostRecentCall.args[1]).toBe(CardForm.STATUS_INFO);
		});

		it("shows a success message on succes", function() {
			var card_form = getCardFormWithFixture();
			spyOn(card_form, 'success');
			spyOn(card_form, 'message');
			card_form.formOpts.success().andCallThrough();
			expect(card_form.message).toHaveBeenCalled();
			expect(card_form.message.mostRecentCall.args[1]).toBe(CardForm.STATUS_SUCCESS);
		});

		it("shows an error message on error", function() {
			var card_form = getCardFormWithFixture();
			spyOn(card_form, 'error');
			spyOn(card_form, 'message');
			card_form.formOpts.error().andCallThrough();
			expect(card_form.message).toHaveBeenCalled();
			expect(card_form.message.mostRecentCall.args[1]).toBe(CardForm.STATUS_ERROR);
		});

	});
});
