define(['jquery', 'lodash'], function($, _) {

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
	var ModuleLoader = function(rootEl) {
		this.rootEl = $(rootEl);
		this.modules = [];
		_.bindAll(this, ['loadModule', 'initModule']);
	};

	ModuleLoader.prototype.loadAll = function() {
		$(document).ready(_.bind(function() {
			this.log("loading all modules from root", this.rootEl);
			$(this.rootEl).find("*[data-module]").andSelf().each(this.loadModule);
		}, this));
	};

	ModuleLoader.prototype.getModulePath = function(moduleName) {
		return "modules/" + moduleName;
	};

	ModuleLoader.prototype.loadModule = function(index, el) {
		this.log("load module", index, el);
		var module_name = $(el).data("module");
		var module_path = this.getModulePath(module_name);

		require([module_path], this.initModule(module_path, el));
	};

	ModuleLoader.prototype.initModule = function(path, el) {
		var that = this;
		return function(module) {
			that.modules.push(module);
			if(module.initModule) {
				module.initModule(el);
				that.log("module initialized");
			} else {
				that.log("module NOT initialized: missing initModule()", path);
			}
		};
	};

	ModuleLoader.prototype.log = function() {
		console.log.apply(console, arguments);
	};

	ModuleLoader.loadAll = function(rootEl) {
		var loader = new ModuleLoader(rootEl);
		loader.loadAll();
	};

	return ModuleLoader;
});
