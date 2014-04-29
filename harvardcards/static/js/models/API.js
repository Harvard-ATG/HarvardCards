define(['module', 'jquery'], function(module, $) {
	/** 
	 * API class for making requests to the server.
	 *
	 * This object is responsible for knowing the API key (if any) and the
	 * root URL to the current verison of the API. In addition to knowing
	 * those two crucial pieces of information, it provides convenience methods
	 * for making requests via jQuery.ajax(). 
	 *
	 * Usage:
	 *
	 * API.ajax({
	 *		url: 'foo/1',
	 *		method: 'GET',
	 *		data: {filter: 'bar'},
	 *		dataType: 'json'
	 *	}).done(function(data, textStatus, xhr) { 
	 *		console.log("api done"); 
	 *	}).fail(function(xhr, textStatus, errorThrown) { 
	 *		console.log("api fail"); 
	 *	});
	 *
	 */
	var API = function(config) {
		config = config || {};
		this.config = {
			url: config.url || '',
			method: config.method || 'GET',
			data: config.data || {},
			dataType: config.dataType || 'json'
		};
	};

	// API key submitted along with requests.
	API.apiKey = module.config().apiKey;

	// API root URL for all resources.
	API.apiRoot = module.config().apiRoot;

	// Returns a fully-qualifiedn API url given a path.
	API.url = function(path) {
		return API.apiRoot + '/' + path;
	};

	// Executes an API request immediately via AJAX.
	API.ajax = function(url, settings) {
		var config = $.extend(settings, {url:url});
		var api = new API(config);
		return api.execute();
	};

	// Convenience methods for updating settings.
	$.each(['url','method','data','dataType'], function(index, attr) {
		API.prototype[attr] = function(value) {
			this.config[attr] = value;
			return this;
		};
	});

	// Executes a request with the current settings and returns 
	// a jQuery.Deferred object.
	// See: http://api.jquery.com/jQuery.Deferred/
	API.prototype.execute = function() {
		var url = API.url(this.config.url);
		var settings = {
			method: this.config.method,
			dataType: this.config.dataType,
			data: this.config.data
		};
		//console.log(url, settings);
		return $.ajax(url, settings);
	};

	return API;
});
