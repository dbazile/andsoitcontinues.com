(function (asic) {

  'use strict'

  //
  // Bootstrapping
  //

  initialize()

  //
  // Internals
  //

  function initialize() {
    console.debug('(portfolio:initialize) subscribing to hashchange events')
    onHashChange()
    window.addEventListener('hashchange', onHashChange)
    asic.transitioner.beforeNext(teardown)
  }

  function onHashChange() {
    // Update the tiles
    var tiles = document.querySelector('.tiles')
    if (location.hash) {
      tiles.classList.add('tiles--hasActiveTile')
    }
    else {
      tiles.classList.remove('tiles--hasActiveTile')
    }
    atoa(document.querySelectorAll('.tiles__tile'))
      .forEach(function (element) {
        if (element.querySelector('a').hash === location.hash) {
          element.classList.add('tiles__tile--isActive')
        }
        else {
          element.classList.remove('tiles__tile--isActive')
        }
      })

    /*
      This is needed because the :target CSS pseudoselector apparently doesn't
      recompute if entering a hashed URL from a history.pushState'd URL.  This
      manifests itself when moving _away_ from portfolio to another route, then
      going back in history.

      Refer to https://bugs.webkit.org/show_bug.cgi?id=83490
     */
    // Update the groups
    atoa(document.querySelectorAll('.narrativeGroup'))
      .forEach(function (element) {
        if (element.id === location.hash.substr(1)) {
          element.classList.add('narrativeGroup--isActive')
        }
        else {
          element.classList.remove('narrativeGroup--isActive')
        }
      })
  }

  function teardown() {
    console.debug('(portfolio:teardown) unsubscribing from hash change events')
    window.removeEventListener('hashchange', onHashChange)
  }
}(window.asic))
