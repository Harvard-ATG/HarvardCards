define(['jquery'], function($) {

    // Constructor 
    var CardTemplatePreview = function(options) {
        this.selectEl = $(options.selectEl); // the <select> element
        this.previewEl = $(options.previewEl); // the <div> element that will hold the preview
        this.url = this.previewEl.data('fetch-url'); // url to fetch preview
        this.defaultText = this.previewEl.data('default-text'); // default text to display
        this.cache = {}; // cache for the template previews to minimize network traffic
    };

    // Initializes the listeners
    CardTemplatePreview.prototype.init = function() {
        this.refresh = $.proxy(this.refresh, this); // bind context 
        this.selectEl.on("change", this.refresh);
    };

    // Updates the view to show the currently selected template.
    CardTemplatePreview.prototype.refresh = function() {
        var card_template_id = this.getSelectedValue();
        this.select(card_template_id);
    };

    // Returns the currently selected value.
    CardTemplatePreview.prototype.getSelectedValue = function() {
        return this.selectEl.find(":selected").val();
    };

    // Selects the template to show.
    CardTemplatePreview.prototype.select = function(cardTemplateId) {
        is_numeric = /^\d+$/.test(cardTemplateId);
        if(is_numeric && cardTemplateId) {
            this.load(cardTemplateId);
        } else {
            this.reset();
        }
    };

    // Updates the preview 
    CardTemplatePreview.prototype.render = function(html) {
        this.previewEl.html(html);
    };

    // Resets the preview to the default text
    CardTemplatePreview.prototype.reset = function() {
        this.render(this.defaultText);
    };

    // Loads the preview for the given card template ID
    CardTemplatePreview.prototype.load = function(cardTemplateId) {
        this.beforeLoad();
        var that = this;
        if(this.cache[cardTemplateId]) {
            this.render(this.cache[cardTemplateId]);
        } else {
            $.ajax({
                url: this.url,
                data: { "card_template_id": cardTemplateId },
                dataType: 'html',
                success: function(data) {
                    that.cache[cardTemplateId] = data;
                    that.render.call(that, data);
                }
            });
        }
    };

    CardTemplatePreview.prototype.beforeLoad = function() {
        this.render('<div class="ajax-loader">loading...</div>');
    };

    return CardTemplatePreview;
});
