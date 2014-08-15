define(['lodash', 'jquery', 'models/API'], function(_, $, API) {
	describe("API", function() {
		it("creates an instance", function() {
			var config = {
				url: '/api/foo',
				method: 'GET',
				data: {foo:'bar'},
				dataType: 'json'
			};
			var api = new API(config);
			expect(api.config).toEqual(config);
		});

		it("constructs urls using the api root", function() {
			var root = '/api';
			API.apiRoot = root;
			var path = "foo/1";
			var url = API.url(path);
			expect(url).toBe([root,path].join('/'));
		});

		it("executes an ajax call", function() {
			var path = "foo/bar";
			var api = new API({url: path});
			var deferred = new $.Deferred();
			deferred.resolve();
			spyOn(api, '_ajax').and.callFake(function() {
				return deferred;
			});
			
			var result = api.execute();
			expect(result).toBe(deferred);	
		});
	});
});
