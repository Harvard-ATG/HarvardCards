define(['lodash','jquery','modules/module-loader'], function(_, $, ModuleLoader) {

	// Creates markup for a single element with an attached module.
	function getModuleHTML(name) {
		return '<div data-module="'+name+'"></div>';
	};

	// Creates markup for a tree of modules since modules can appear
	// anywhere in the DOM.
	function getModulesHTML(modules) {
		return _.reduce(modules, function(html, m) {
			if(typeof m === 'string') {
				return html + getModuleHTML(m);
			} 
			return html + '<div>' + getModulesHTML(m) + '</div>';
		}, '');
	}

	// Returns a fixture that is a jQuery object containing DOM nodes with modules.
	function getFixture(modules) {
		return $("<div>").html(getModulesHTML(modules));
	}

	describe("ModuleLoader", function() {
		it("creates an instance with a root element", function() {
			var fixture = $("<div>");
			var module_loader = new ModuleLoader(fixture);

			// Compare the DOM elements (*not* jQuery objects) for equality
			expect(module_loader.rootEl.get(0)).toBe(fixture.get(0));
		});

		it("finds modules to load", function() {
			var modules = ['foo', 'bar', ['a',['b',['c']]], 'baz'];
			var fixture = getFixture(modules);
			var module_loader = new ModuleLoader(fixture);
			var found = module_loader.findModules();

			expect(_.pluck(found, 'name')).toEqual(_.flatten(modules));
		});

		it("loads modules", function() {
			var modules = ['foo', 'bar', 'baz'];
			var fixture = getFixture(modules);
			var module_loader = new ModuleLoader(fixture);

			spyOn(module_loader, 'loadModule');
			module_loader.loadAll();
			expect(module_loader.loadModule).toHaveBeenCalled();
			expect(module_loader.loadModule.calls.length).toEqual(modules.length);
		});
	});
});
