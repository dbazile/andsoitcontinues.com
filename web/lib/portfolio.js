(function (bazile, atoa) {

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
    window.addEventListener('hashchange', onHashChange)
    bazile.transitioner.beforeNext(teardown)
    onHashChange()

    /*
      This is needed because the :target CSS pseudoselector apparently doesn't
      recompute if entering a hashed URL from a history.pushState'd URL.  This
      manifests itself when moving _away_ from portfolio to another route, then
      going back in history.

      Now all I need to figure out is how to avoid the stinkin' 15px "sink" when
      bouncing the hash... >_<

      Refer to https://bugs.webkit.org/show_bug.cgi?id=83490
     */
    if (location.hash) {
      console.debug('(portfolio:initialize) bouncing hash')
      location.replace(location.href)
    }
  }

  function onHashChange() {
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
  }

  function teardown() {
    console.debug('(portfolio:teardown) unsubscribing from hash change events')
    window.removeEventListener('hashchange', onHashChange)
  }
}(window.bazile, window.atoa))
