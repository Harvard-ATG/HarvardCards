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
			var editor = new InlineEditor(fixture, {});
			expect(editor.el.get(0)).toBe(fixture.get(0));
		});

		it("executes callback on edit", function() {
			var editor = null; 
			var result = null;
			var new_value = 'bar';
			var fixture = getFixture('foo');
			var options = {
				edit: function() {
					var deferred = new $.Deferred();
					deferred.resolve(); // resolve immediately
					return deferred;
				},
				success: function() {},
				error: function() {}
			};

			spyOn(options, 'success');
			spyOn(options, 'error');
			spyOn(options, 'edit').and.callThrough();

			editor = new InlineEditor(fixture, options);
			result = editor.handleEdit(editor, new_value, {});

			expect(result).toBe(new_value);
			expect(options.edit).toHaveBeenCalled();
			expect(options.success).toHaveBeenCalled();
			expect(options.error).not.toHaveBeenCalled();
		});
	});
});
