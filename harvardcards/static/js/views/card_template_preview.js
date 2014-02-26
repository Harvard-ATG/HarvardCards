define(['jquery'], function($) {
    var CardTemplatePreview = function(options) {
        this.selectEl = $(options.selectEl);
        this.previewEl = $(options.previewEl);
        this.url = this.previewEl.data('fetch-url');
		this.defaultText = this.previewEl.html();
        this.cache = {}; // cache the template previews to minimize network traffic
    };

    CardTemplatePreview.prototype.init = function() {
        var that = this;
        this.selectEl.on("change", function() {
            var card_template_id = $(this).find(":selected").val();
			if(card_template_id) {
				that.loadPreview(card_template_id);
			} else {
				that.resetPreview();
			}
        });
    };

    CardTemplatePreview.prototype.updatePreview = function(html) {
        this.previewEl.html(html);
    };

	CardTemplatePreview.prototype.resetPreview = function() {
		this.updatePreview(this.defaultText);
	};

    CardTemplatePreview.prototype.loadPreview = function(cardTemplateId) {
        var that = this;
        if(this.cache[cardTemplateId]) {
            this.updatePreview(this.cache[cardTemplateId]);
        } else {
            $.ajax({
                url: this.url,
                data: { "card_template_id": cardTemplateId },
                dataType: 'html',
                success: function(data) {
                    that.cache[cardTemplateId] = data;
                    that.updatePreview.call(that, data);
                }
            });
        }
    };

    return CardTemplatePreview;
});
