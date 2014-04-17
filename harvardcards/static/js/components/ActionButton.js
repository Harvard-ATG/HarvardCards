define(['jquery'], function($) {

	/**
	 * Creates an action button object intended to be attached to a button element.
	 * Handles common responsibilities such as setting up click handlers and POSTing data
	 * to a URL. The object provides a hooks before and after the action is triggered.
	 *
	 * Usage:
	 *
	 * var button = new ActionButton($("#button"), {
	 *      before: function(data) {
	 *          data['foo'] = 1;
	 *          data['bar'] = 2;
	 *          return true;
	 *      },
	 *      after: function() {
	 *          alert("success!");
	 *      }
	 * });
	 *
	 * button.doAction();
	 *
	 */
	var ActionButton = function(el, options) {
		options = options || {};
		if(!el) {
			throw new Error("missing element");
		}

		this.el = $(el);
		this.options = options;
		this.doAction = $.proxy(this.doAction, this);
		this.completeAction = $.proxy(this.completeAction, this);
		this.init()
	};

	// Initializes the object and sets up click handler
	ActionButton.prototype.init = function() {
		this.actionUrl = this.options.url || this.el.data('action-url');
		this.beforeAction = this.options.before || function() { return true; };
		this.afterAction = this.options.after || function() {};
		this.el.on("click", this.doAction);
	};

	// Executes the action.
	ActionButton.prototype.doAction = function() {
		var that = this, can_continue = false, data = {};

		can_continue = this.beforeAction(data);
		if(!can_continue) {
			return false;
		}

		if(this.actionUrl) {
			$.ajax({
				url: this.actionUrl,
				type: "POST",
				dataType: "json",
				data: data,
				success: function(data, textStatus, xhr) {
					that.afterAction(true, data);
				},
				error: function(xhr, textStatus) {
					that.afterAction(false, textStatus);
				}
			});
		} else {
			this.afterAction(true);
		}

		return true;
	};

	return ActionButton;
});