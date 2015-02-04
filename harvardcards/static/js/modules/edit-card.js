define(['jquery', 'views/CardForm'], function($, CardForm) {

    function setup_file_url_switch() {
        $('select[data-switch]').each(function(idx, el) {
        console.log("setup", idx, el);
            var url_selector = $(el).data("switch-url");
            var file_selector = $(el).data("switch-file");
            $(el).on("change", function() {
                var source_type = $(el).val();
                $('input[name='+file_selector+']')[source_type=='U'?'hide':'show']();
                $('input[name='+url_selector+']')[source_type=='U'?'show':'hide']();
                console.log("change", idx, el, source_type, "this", this);
            });
        });
    }

    return {
        initModule: function(el) {
            var cardform = new CardForm({
                "formEl": "#cardForm",
                "formMessageEl": "#cardForm .formMessage"
            });
            cardform.init();

            setup_file_url_switch();
        }
    };
});
