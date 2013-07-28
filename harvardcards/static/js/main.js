requirejs.config({
	paths: {
		'jquery' : 'http://code.jquery.com/jquery-1.10.1.min.js',
		'lodash' : '//cdnjs.cloudflare.com/ajax/libs/lodash.js/1.3.1/lodash',
		'bootstrap' : '//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min'
	},
	shim: {
		'jquery' : '$',
		'lodash' : {
			exports: '_'
		}
	}
});

