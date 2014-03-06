define(['jquery', 'lodash'], function($, _) {

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
