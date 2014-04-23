define(['lodash','jquery','components/InlineEditor'], function(_, $, InlineEditor) {
	function getFixture(content) {
		return $('<div/>').html(content);
	}

	function getEditor(content, url, name) {
		var fixture = getFixture(content);
		var options = {
			url: url,
			name: name
		};
		return new InlineEditor(fixture, options);
	}

	describe("InlineEditor", function() {
		it("creates an instance", function() {
			var fixture = getFixture('xyz');
			var options = {
				url: '/api/foo',
				name: 'foo'
			};
			var editor = new InlineEditor(fixture, options);
			expect(editor.el.get(0)).toBe(fixture.get(0));
			expect(editor.url).toBe(options.url);
			expect(editor.name).toBe(options.name);
		});

		it("executes callback on edit", function() {
			var old_value = "oldvalue", new_value = "newvalue";
			var fixture = getFixture(old_value);
			var options = {
				url: '/api/foo',
				name: 'foo',
				success: function() {},
				error: function() {}
			};
			var editor, result;

			spyOn(options, 'success');
			spyOn(options, 'error');

			editor = new InlineEditor(fixture, options);

			spyOn(editor, 'ajax').andCallFake(function() {
				var deferred = new $.Deferred();
				deferred.resolve(); // resolve immediately
				return deferred;
			});

			result = editor.handleEdit(editor, new_value, {});

			expect(result).toBe(new_value);
			expect(editor.ajax).toHaveBeenCalled();
			expect(options.success).toHaveBeenCalled();
			expect(options.error).not.toHaveBeenCalled();
		});
	});
});