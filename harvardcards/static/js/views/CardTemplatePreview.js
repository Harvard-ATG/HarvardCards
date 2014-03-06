define(['jquery'], function($) {

    // Constructor 
    var CardTemplatePreview = function(options) {
        this.selectEl = $(options.selectEl); // the <select> element
        this.previewEl = $(options.previewEl); // the <div> element that will hold the preview
        this.url = this.previewEl.data('fetch-url'); // url to fetch preview
        this.defaultText = this.previewEl.html(); // default text to display
        this.cache = {}; // cache for the template previews to minimize network traffic
    };

    // Initializes the listeners
    CardTemplatePreview.prototype.init = function() {
		this.onSelect = $.proxy(this.onSelect, this); // bind context 
        this.selectEl.on("change", this.onSelect);
    };

	// Handles the select element change event.
	CardTemplatePreview.prototype.onSelect = function() {
		var card_template_id = this.selectEl.find(":selected").val();
		this.select(card_template_id);
	};

	// Selects the template to show.
	CardTemplatePreview.prototype.select = function(cardTemplateId) {
		if(cardTemplateId) {
			this.load(cardTemplateId);
		} else {
			this.reset();
		}
	};

    // Updates the preview 
    CardTemplatePreview.prototype.update = function(html) {
        this.previewEl.html(html);
    };

    // Resets the preview to the default text
    CardTemplatePreview.prototype.reset = function() {
        this.update(this.defaultText);
    };

    // Loads the preview for the given card template ID
    CardTemplatePreview.prototype.load = function(cardTemplateId) {
        var that = this;
        if(this.cache[cardTemplateId]) {
            this.update(this.cache[cardTemplateId]);
        } else {
            $.ajax({
                url: this.url,
                data: { "card_template_id": cardTemplateId },
                dataType: 'html',
                success: function(data) {
                    that.cache[cardTemplateId] = data;
                    that.update.call(that, data);
                }
            });
        }
    };

    return CardTemplatePreview;
});
