define(['jquery', 'views/CardForm'], function($, CardForm) {
    return {
        initModule: function(el) {
                        var cardform = new CardForm({
                            "formEl": "#cardForm",
                            "formMessageEl": "#cardForm .formMessage"
                        });
                        cardform.init();
                    }
    };
});

function switch_upload_image_type(sel)
{
    var file_input = document.getElementById("file_upload_type");
    var url_input = document.getElementById("url_upload_type");
    if (sel.value == "U")
    {
        file_input.style.display = "none";
        url_input.style.display = "block";
    }
    else
    {
        file_input.style.display = "block";
        url_input.style.display = "none";
    }
}
