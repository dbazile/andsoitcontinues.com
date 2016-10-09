(function() {
	var asic = {
		interfaces: {},
		functions: {}
	};

	/**
	 * Page initializer
	 */
	window.onload = function() {

	};

	// Initialize namespace
	window.asic = asic;

	// IE8, wherefore art thou IE8?
	if (!String.prototype.trim)
		String.prototype.trim = function() { return this.replace(/(^\s+|\s+$)/g, ''); };

})();
