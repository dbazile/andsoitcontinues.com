(function (atoa) {

  'use strict'

  var CLASS_STATE_INITIAL = 'state--initial'
  var CLASS_STATE_ERROR = 'state--error'
  var CLASS_STATE_HAS_RESULTS = 'state--hasResults'
  var CLASS_STATE_NO_RESULTS = 'state--noResults'
  var CLASS_STATE_SEARCHING = 'state--searching'
  var CLASS_TAG_MATCH = 'tag--matches'

  var _lastCancelToken, _templateForBlog, _templateForPortfolio

  //
  // Bootstrapping
  //

  initialize()

  //
  // Internals
  //

  function initialize() {
    collectTemplates()

    var query = getQueryFromURL()
    if (query) {
      updateQueryDOM(query)
      search(query)
    }

    window.addEventListener('popstate', onPopState)
    document.querySelector('form').addEventListener('submit', onSubmit)
    atoa(document.querySelectorAll('.placeholder__dismissButton')).forEach(function (button) {
      button.addEventListener('click', onDismiss)
    })
  }

  function appendResult(result) {
    var results = document.querySelector('.results')
    var node = _templateForBlog.cloneNode(true)
    node.querySelector('.result__subject').textContent = result.subject
    node.querySelector('.result__hyperlink').href = result.uri
    node.querySelector('.result__description').textContent = result.description
    var tags = node.querySelector('.result__tags')
    var query = getQueryFromURL()
    result.tags.map(function (s) {
      var tag = document.createElement('li')
      tag.textContent = s
      if (query === 'tagged:' + s) {
        tag.className = CLASS_TAG_MATCH
      }
      tags.appendChild(tag)
    })
    results.appendChild(node)
  }

  function collectTemplates() {
    _templateForBlog = document.querySelector('.result--blog')
    _templateForBlog.parentNode.removeChild(_templateForBlog)
    _templateForPortfolio = document.querySelector('.result--portfolio')
    _templateForPortfolio.parentNode.removeChild(_templateForPortfolio)
  }

  function onDismiss() {
    reset()
    document.documentElement.className = CLASS_STATE_INITIAL
  }

  function reset() {
    var results = document.querySelector('.results')
    while (results.firstChild) {
      results.removeChild(results.firstChild)
    }
  }

  function createCancelToken() {
    if (_lastCancelToken) {
      _lastCancelToken.cancelled = true
    }
    _lastCancelToken = {cancelled: false}
    return _lastCancelToken
  }

  function getQueryFromDOM() {
    return document.querySelector('input').value
  }

  function getQueryFromURL() {
    return decodeURIComponent(location.search.substr(1))
      .replace(/^tagged=/, 'tagged:')
      .replace(/^keyword=/, '')
  }

  function onPopState() {
    var query = getQueryFromURL()
    updateQueryDOM(query)
    search(query)
  }

  function onSubmit(event) {
    event.preventDefault()
    var query = document.querySelector('input').value

    updateQueryURL(query)
    search(query)
  }

  function search(query) {
    console.debug('Searching for `%s`', query)
    var xhr = new XMLHttpRequest()
    var endpoint = document.querySelector('form').action
    xhr.open('GET', endpoint + '?query=' + encodeURIComponent(query))

    var token = createCancelToken()
    xhr.onload = function () {
      try {
        if (token.cancelled) {
          return
        }

        reset()
        if (xhr.status !== 200) {
          throw Error('API returned non-200')
        }

        var response = JSON.parse(xhr.responseText)
        document.querySelector('.metrics__count').textContent = response.results.length
        document.querySelector('.metrics__query').textContent = query
        response.results.forEach(appendResult)
        setState(response.results.length ? CLASS_STATE_HAS_RESULTS : CLASS_STATE_NO_RESULTS)
      }
      catch (err) {
        console.error('Search failed:', err)
        setState(CLASS_STATE_ERROR)
      }
    }
    setState(CLASS_STATE_SEARCHING)
    xhr.send()
  }

  function updateQueryDOM(query) {
    document.querySelector('input').value = query
  }

  function updateQueryURL(query) {
    var href = location.href.replace(/\?.*$/, '')
    if (query.match(/^tagged:/)) {
      href += '?tagged=' + encodeURIComponent(query.replace('tagged:', ''))
    }
    else {
      href += '?keyword=' + encodeURIComponent(query)
    }
    history.pushState(null, null, href)
  }

  function setState(state) {
    document.documentElement.className = state
  }

}(window.atoa))
