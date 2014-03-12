define(['jquery'], function() {
	var GLOBAL_DEBUG_CONST = "APP_FLASH_DEBUG";

	// Mixin to add simple debugging facilities to an object or class.
	var DebugMixin = {
		// Enables tracing with debugging.
		enableDebugTrace: function() {
			this.debugTracing = true;
		},
		// Sets debug to true.
		enableDebug: function() {
			this.debugging = true;
		},
		// Sets debug to false.
		disableDebug: function() {
			this.debugging = false;
		},
		// Returns true/false of the local debug value if it is defined, 
		// otherwise the status of global debugging.
		isDebugEnabled: function() {
			if(this.debugging === false || this.debugging === true) {
				return this.debugging;
			}
			return !!window[GLOBAL_DEBUG_CONST]; // coerce to boolean
		},
		// Logs a message if debugging is enabled. 
		// Optionally shows a trace after the message if tracing is enabled.
		// Optionally shows a prefix in the log output.
		debug: function() {
			var args = Array.prototype.slice.call(arguments, 0);
			var prefix = this.debuggingPrefix || (this.constructor && this.constructor.name);
			if(prefix) {
				args.unshift("DEBUG::" + prefix);
			}
			if(this.isDebugEnabled()) {
				console.log.apply(console, args);
				if(this.debugTracing) {
					console.trace();
				}
			}
		}
	};

	return DebugMixin;
});
