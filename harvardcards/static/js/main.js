requirejs.config({
	paths: {
		'jquery' : 'http://code.jquery.com/jquery-1.10.1.min.js',
		'bootstrap' : '//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js'
	},
	shim: {
		'jquery' : '$'
	}
});

require(['jquery'], function($) {
	//$ points to jQuery
});