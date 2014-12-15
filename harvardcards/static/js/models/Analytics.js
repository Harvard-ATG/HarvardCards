define(['lodash', 'models/API'], function(_, API) {
	var DEBUG = true;

	/**
	 * Analytics class for gathering and savings tracking data.
	 *
	 * Tracking data is internally buffered and sent in batches 
	 * to smooth out bursts of activity, however client code
	 * doesn't need to care about the details.
	 *
	 * Usage:
	 *
	 * Analytics.run(); // starts polling process
	 * Analytics.stop(); // stop polling process
	 * Analytics.send(); // flushes statement buffer to server
	 *
	 * Analytics.trackCard(card_id, mode); // track card activity
	 *
	 */
	var Analytics = {
		/**
		 * Statement buffer; an array of objects.
		 */
		statements: [],
		/**
		 * Delay (ms) between POSTing requests to the analytics server. 
		 */
		delay: 2000,
		/**
		 * Current ID for window.setTimeout()
		 */
		timeoutID: null, 
		/**
		 * Tracks a statement.
		 *
		 * @param {object} data 
		 * @return this
		 */
		track: function(data) {
			data = data || {};
			if("verb" in data && "object" in data) {
				this.statements.push(data);
			} else {
				console.log("invalid tracking data: ", data, "; missing verb/object");
			}
			return this;
		},
		/**
		 * Sends all statements that are in the buffer.
		 *
		 * @return this
		 */
		send: function() {
			var statements = this.statements.slice(0); 
			if(statements.length > 0) {
				this.debug("send", statements);
				API.ajax("analytics/track", {
					method: "POST",
					data: {
						"statements": JSON.stringify(statements)
					}
				});
				this.statements = [];
			}
			return this;
		},
		/**
		 * Runs the polling mechanism that sends statements that have
		 * accumulated periodically.
		 *
		 * @return this
		 */
		run: function() {
			this.debug("run", this.delay);
			this.send();
			this.timeoutID = window.setTimeout(this.run, this.delay);
			return this;
		},
		/**
		 * Stops sending tracking data, but statements will still accumulate in the buffer.
		 *
		 * @return this
		 */
		stop: function() {
			this.debug("stop", this.timeoutID);
			if(this.timeoutID !== null) {
				window.clearTimeout(this.timeoutID);
			}
			return this;
		},
		/**
		 * Utility function to print debug statements to the console.
		 *
		 * @return this
		 */
		debug: function() {
			if(DEBUG) {
				console.log.apply(console, arguments);
			}
			return this;
		},
		/**
		 * Track a card that is viewed.
		 *
		 * @param {string} card_id 
		 * @param {string} mode quiz or review
		 * @return this
		 */
		trackCard: function(card_id, mode) {
			var now = new Date();
			var iso_timestamp = "";

			if(now.toISOString) {
				 iso_timestamp = now.toISOString();
			}

			var data = {
				"verb": "viewed", 
				"object": "card",
				"context": {
					"card_id": card_id,
					"mode": mode,
					"userAgent": window.navigator.userAgent,
					"screenWidth": window.screen.width
				},
				"timestamp": iso_timestamp
			};

			this.track(data);

			return this;
		}
	};

	_.bindAll(Analytics, ['track','run','stop','send','trackCard']);

	return Analytics;
});
