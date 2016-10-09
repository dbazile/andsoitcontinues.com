(function () {
  /* global hljs */

  'use strict'


  // Activate syntax highlighting
  atoa(document.querySelectorAll('pre'))
    .forEach(function (node) {
      var language = node.querySelector('code').getAttribute('class')
      // Only highlight contexts that are explicitly marked
      if (language) {
        node.classList.add(language)
        hljs.highlightBlock(node)
      }
    })

}())
