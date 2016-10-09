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
    onHashChange()
    window.addEventListener('hashchange', onHashChange)
    asic.transitioner.beforeNext(teardown)
  }

  function onHashChange() {
    console.debug('(portfolio:onHashChange) event fired')
    var container = document.querySelector('.tiles')
    if (location.hash) {
      container.classList.add('tiles--hasActiveTile')
    }
    else {
      container.classList.remove('tiles--hasActiveTile')
    }
    var tiles = atoa(document.querySelectorAll('.tiles__tile'))
    tiles.forEach(function (tile) {
      if (tile.querySelector('a').hash === location.hash) {
        tile.classList.add('tiles__tile--isActive')
        var y = document.querySelector('.ui').offsetTop
        window.scrollTo(0, y)
      }
      else {
        tile.classList.remove('tiles__tile--isActive')
      }
    })
  }

  function teardown() {
    console.debug('(portfolio:*) unsubscribing from hash change events')
    window.removeEventListener('hashchange', onHashChange)
  }
}(window.asic))
