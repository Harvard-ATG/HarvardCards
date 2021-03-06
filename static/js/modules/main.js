define(['jquery', 'jquery.cookie', 'jquery.appendAround', 'jquery.scrollTo'], function(jquery, jqueryCookie, jqueryAppend, jqueryScrollTo) {
	return {
		initModule: function(el) {
			this.setupCSRF();
			this.setupAppNav();
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
		
			// Scroll to the visible mobile nav menu
			$("#mobileMenu").on("click", function(e) {
				var target = $('[data-set=mobileNav]:visible');
				if(target.length == 1) {
					$("html,body").scrollTo(target, 300);
				}
			});

            var inIframe = function(){
                try {
                    return window.self !== window.top;
                } catch (e) {
                    return true;
                }
            };
            // if the content is in an iFrame, we don't want to show the header, which defaults to hidden
            if(!inIframe()){
                $('#fc_headerWrapper').show();
            }
		}
	};
});
