Date:     2015-04-12
Subject:  JSBin Experiments
Tags:     experimentation, animation, css, javascript, svg, jsbin
Abstract: Posting a bunch of recent experiments and prototypes.

I've been using [JSBin](http://www.jsbin.com) to do a lot of prototyping and experimentation recently.

## EmberJS

These are mostly "do-overs" from work things.

#### [Sliding menu drawer with animations](http://jsbin.com/nedaro/5/edit?html,js,output)<sup>1</sup>

#### [Barebones drag and drop](http://jsbin.com/lekanu/2/edit?html,css,js,output)<sup>2</sup>



## Animation

#### [Drawing line segments (SVG + JS)](http://jsbin.com/hilico/1/edit?html,css,js,output)

#### [Weird monitor (Canvas + JS)](http://jsbin.com/figulu/1/edit?html,css,js,output)

#### [Spinning box (SVG + JS)](http://jsbin.com/dacepe/1/edit?html,css,js,output)

#### [Spinning box (SVG + CSS)](http://jsbin.com/potiqe/2/edit?html,css,output)

#### [CSS transitions on SVG inside of Anchor Tag](http://jsbin.com/xotutu/2/edit?html,css,output)<sup>3</sup>

#### [Wiggling Key (SVG + CSS)](http://jsbin.com/wapaba/1/edit?html,css,output)



## Notes

1. Updated 2015-04-30: Using `transitionend` instead of a timeout (h/t JS).

2. Here, I try to put together the simplest drag and drop as I could.  The one I did at work evented off of `dragenter`, which proved to be [a total pain in the butt](http://jsbin.com/jotepa/2/edit?html,css,js,output).
Incidentally, while doing this I also learned that a bunch of the native DOM events are [pre-aliased into the Ember view layer](http://guides.emberjs.com/v1.10.0/understanding-ember/the-view-layer/#toc_adding-new-events).

3. This is directly related to one bug on this site. :)
