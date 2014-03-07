define(['jquery', 'lodash', 'mixins/debug-mixin'], function($, _, DebugMixin) {

	/**
	 * The ModuleLoader is responsible for finding and loading modules
	 * declared in HTML markup.
	 *
	 * It works by finding all elements that have a "data-module" attribute
	 * and then loading and initializing the module. Modules are loaded
	 * asynchronously using requirejs. Modules are defined the same way
	 * any requirejs module is defined with the only requirement being that
	 * it export a method called "initModule()". The initModule() method
	 * is called after the module is loaded. 
	 *
	 * Modules can be thought of as the wrapper or glue around a set of controllers,
	 * models, and views that add behavior to some subset of the DOM. Typically,
	 * the element on which the module is defined in the HTML markup sets the
	 * scope of the module's responsibility. 
	 *
	 * The goal of this is to enforce *strict* separation between the HTML
	 * markup and javascript. 
	 *
	 * Example:
	 *
	 *		<body data-module="main"> ... </body>
	 *
	 *		The ModuleLoader will then load: js/modules/main.js and call
	 *		initModule(), passing it the <body> element.
	 *
	 */
	function ModuleLoader(rootEl) {
		this.rootEl = $(rootEl);
		_.bindAll(this, ['loadModule', 'createModuleCallback']);
	};

	// Mixin debugging behavior.
	_.extend(ModuleLoader.prototype, DebugMixin);

	// Returns the requireJS path to the module given the module name.
	ModuleLoader.prototype.getModulePath = function(moduleName) {
		return "modules/" + moduleName;
	};

	// Loads all modules.
	ModuleLoader.prototype.loadAll = function() {
		_(this.findModules()).each(function(module) {
			this.loadModule(module.name, module.path, module.el);
		}, this);
	};

	// Finds all elements from the root element that have a data-module attribute
	// and returns a list of objects with the module info.
	ModuleLoader.prototype.findModules = function() {
		var that = this, modules = [];
		this.rootEl.find("*[data-module]").andSelf().each(function(index, el) {
			var name = $(el).data("module"); 
			if(name) {
				modules.push({el: el, name: name, path: that.getModulePath(name)});
			}
		});
		return modules;
	};

	// Delegates the loading to the global require() function.
	ModuleLoader.prototype.loadModule = function(name, path, el) {
		this.debug("load module", path, el);
		require([path], this.createModuleCallback(path, el));
	};

	// Returns a function that will call the initModule() method on the module object.
	ModuleLoader.prototype.createModuleCallback = function(path, el) {
		return _.bind(function(module) {
			if(module.initModule) {
				module.initModule(el);
				this.debug("initialized module", path);
			} else {
				this.debug("failed to initialize module: missing initModule()", path);
			}
		}, this);
	};

	// Class method for convenience.
	ModuleLoader.loadAll = function(rootEl) {
		$(document).ready(function() { 
			var loader = new ModuleLoader(rootEl);
			loader.loadAll();
		});
	};

	return ModuleLoader;
});
