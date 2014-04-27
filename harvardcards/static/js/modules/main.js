define(['jquery', 'jquery.cookie', 'jquery.appendAround', 'views/urlManipulate'], function(jquery, jqueryCookie, jqueryAppend, urlManipulate) {
    function instructorEditMode(href, enabled) {
        var href = location.href;
        if(enabled) {
            return urlManipulate.addParameter(href, 'instructor', 'edit', false);
        } 
        return urlManipulate.removeURLParameter(href, 'instructor');
    }

	return {
		initModule: function(el) {
			this.setupCSRF();
			this.setupAppNav();
            this.setupInstructorModeButton("#viewMode", false);
            this.setupInstructorModeButton("#editMode", true);
		},
		setupInstructorModeButton: function(el, enabled){
            $(el).on("click", function() {
                location.href = instructorEditMode(location.href, enabled);
                return false;
            });
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
