define(['jquery', 'views/CardForm'], function($, CardForm) {

    $('#add_another').click(
        function(){
            $('#add_another_val').val('1');
            $('#submit_form').click();
        }
    )
    function setup_file_url_switch() {
        $('select[data-switch]').each(function(idx, el) {
            var url_selector = $(el).data("switch-url");
            var file_selector = $(el).data("switch-file");
            $(el).on("change", function() {
                var source_type = $(el).val();
                $('input[name='+file_selector+']')[source_type=='U'?'hide':'show']();
                $('input[name='+url_selector+']')[source_type=='U'?'show':'hide']();
            });
        });
    }

    function setup_math_preview() {
        $('input[data-math="true"]').each(function(index) {
            var $math_preview = $("#math_"+this.name);
            $math_preview.html($(this).val())
            update_math($math_preview[0].id)
        }).on('change', function(evt) {
            var $target = $(evt.target);
            var $math_preview = $("#math_"+evt.target.name);
            $math_preview.html($target.val())
            update_math($math_preview[0].id);
        });
    }
    
    function update_math(element_id) {
        if (MathJax) {
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, element_id]);
        }
    }
    
    return {
        initModule: function(el) {
            var cardform = new CardForm({
                "formEl": "#cardForm",
                "formMessageEl": "#cardForm .formMessage"
            });
            cardform.init();
            
            setup_file_url_switch();
            
            setup_math_preview();
        }
    };
});
