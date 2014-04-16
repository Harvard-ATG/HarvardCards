define(['jquery', 'jquery.cookie', 'jquery.appendAround', 'views/urlManipulate'], function(jquery, jqueryCookie, jqueryAppend, urlManipulate) {
	return {
		initModule: function(el) {
			this.setupCSRF();
			this.setupAppNav();
			this.setupEditBtn();
			this.setupViewBtn();
		},
		setupViewBtn: function(){
		    $('#viewMode').click(function(){
                location.href = urlManipulate.removeURLParameter(this.href, 'instructor');
                return false;
            })
		},

		setupEditBtn: function(){
		    $('#editMode').click(function(){
                location.href=urlManipulate.addParameter(this.href,'instructor','edit', false);
                return false;
            })
		},

		setupCSRF: function() {
			var csrftoken = $.cookie('csrftoken');
			function csrfSafeMethod(method) {
				// these HTTP methods do not require CSRF protection
				return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
			}
			$.ajaxSetup({
				crossDomain: false, // obviates need for sameOrigin test
				beforeSend: function(xhr, settings) {
					if (!csrfSafeMethod(settings.type)) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				}
			});
		},
		setupAppNav: function() {
			// The following is a jQuery plugin for responsive-design. 
			//
			// Here we are using it to ensure that the appropriate navigation structure
			// is visible to the user given that CSS media queries will hide/show 
			// the "nav" containers in the DOM.
			// 
			// See also: https://github.com/filamentgroup/AppendAround
			$(".appNav").appendAround(); 
		}
	};
});
