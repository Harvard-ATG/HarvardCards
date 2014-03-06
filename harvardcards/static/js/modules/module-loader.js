define(['jquery', 'lodash'], function($, _) {

	var ModuleLoader = function(rootEl) {
		this.rootEl = $(rootEl);
		this.modules = [];
		_.bindAll(this, ['loadModule', 'initModule']);
	};

	ModuleLoader.prototype.loadAll = function() {
		this.log("loading all modules from root", this.rootEl);
		$(this.rootEl).find("*[data-module]").andSelf().each(this.loadModule);
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
			that.log("loaded module", path,  el);
			that.modules.push(module);
			module.init(el);
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
