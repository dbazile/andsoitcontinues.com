(function (asic) {
	asic.ImageLoupe = function(elementId) {
		var self      = this,
			widget    = document.getElementById(elementId);

		var imageElement   = widget.getElementsByTagName('img').item(0),
			headingElement = widget.getElementsByTagName('h2').item(0),
			captionElement = widget.getElementsByTagName('p').item(0),
			buttonClose    = widget.getElementsByTagName('button').item(0);

		/**
		 * Closes the widget
		 */
		var closeWidget = function () {
			widget.className = 'closed';
		};

		/**
		 * Loads and displays an image in the loupe
		 *
		 * @param {string} url
		 * @param {string} heading
		 * @param {string} caption
		 */
		var displayImage = function (url, heading, caption) {

			// Set "loading" status
			widget.className = 'loading';

			var preload = new Image();

			// Once the image is preloaded, hide the "loading" status
			preload.onload = function(event) {
				widget.className = '';
			};

			preload.src = url;
			imageElement.src = preload.src;
			imageElement.alt = heading;

			headingElement.innerHTML = heading;
			captionElement.innerHTML = caption;

		};

		//
		// ATTACH EVENTS
		//

		/**
		 * Closes the widget when clicked
		 * @param {Event} event
		 */
		buttonClose.onclick = function(event) {
			closeWidget();
		};

		/**
		 * Closes the widget when user hits esc key
		 * @param {Event} event
		 */
		window.onkeydown = function (event) {
			if (27 === event.keyCode) {
				console.info('Received <ESC> key event;  closing widget');
				closeWidget();
			}
		};

		//
		// RETURN PUBLIC METHODS
		//
		return { displayImage: displayImage, closeWidget: closeWidget };
	};

	var originalOnLoadMethod = window.onload;
	window.onload = function() {

		// Let's be good neighbors to anything else that is living in window.onload()
		originalOnLoadMethod();

		var loupe = new asic.ImageLoupe('loupe');

		// Find all portfolio-button anchors and attach click events
		var buttons = document.getElementsByTagName('a'),
			currentButton,
			currentCaption,
			currentHeading,
			currentUrl;

		for (var i=0; i<buttons.length; i++) {
			currentButton = buttons.item(i);

			if (currentButton.className.match('portfolio-button')) {

				currentButton.onclick = function(event) {
					var dataContext = event.target.parentElement.parentElement;

					// Get the captions, headings and URLs please
					var heading = dataContext.getElementsByTagName('h2').item(0).innerHTML,
						caption = dataContext.getElementsByTagName('p').item(0).innerHTML,
						url = event.target.href;

					loupe.displayImage(url, heading, caption);

					event.preventDefault();

				};
			}
		}

		// Export the loupe
		asic.loupe = loupe;
	};
})(window.asic);
