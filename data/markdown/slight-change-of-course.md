---
date:    2013-08-01
subject: Slight Change of Course
tags:
    - blog
    - python
    - php
    - refactoring
abstract: |
    So, the plan for converting my makeshift CMS, blog.php, over to
    Python has been shelved indefinitely.
---

From a technical standpoint, there's not much stopping me from rewriting the entire project in Python.  It might take me a few weeks and a whole mess of spit and duct tape, but I know I could do it.  But for the following reasons, I have concluded that it would be the equivalent of performing rote coding exercises instead of actual learning and might not be the best use of my already splintered free time.

## Covering Old Ground

Essentially, this project would just be busy work of reimplementing the same patterns from the previous build with a few "lessons learned" tweaks tossed in for good measure.  And those tweaks would come at the heavy cost of increased testing time and increased time to completion.  I spent an entire evening caught up in the design phase, overwhelmed by feature creep. "Oo shiny, add it to the list".  "Definitely going to need that, add it to the list".  Again, this is not learning.

## Reinventing the Wheel

I thought about all of the distinct components required to do this properly.  Low-level CRUD is of course very straightforward but for a blog tool to be anything more than Notepad.exe in the browser, there's a slightly higher level of functionality required.

One example would be that I needed some type of presentation shorthand syntax, much like Markdown.  So I'd either have to write a complex and doubtlessly highly buggy string filter to split by newline where it doesn't find HTML block tags and append P tags or whatever or use a third party library.  Or, HTML templating in general.  Do I just use whatever Django uses?  Do I write my own custom blocks?

And now that I'm already walking the dark path of outsourcing functionality by considering third party tools, why stop there?  Why not pull in all kinds of other different components and just Frankenstein that mess together?

## Time is Money

Okay, so I don't actually think that `time == money`, but time is finite and a scarce resource I can no longer afford to use unstrategically.  With my oldest getting ready to go to school in two weeks, I accept that my family needs my time when I'm at home.  I don't want to spend it cheaply grinding away on something I've already solved just to prove some point.  blog.php is approximately at 7,000+ LOC as of today.  That's a lot of boilerplate to transcribe.

## Tumblr's got it Goin' On

I like it for several reasons, most notably the fact that it supports custom domains out of the box and posting different types of media.  The fact that it has an iPhone app is just the bees knees.  Another developer that I respect also has a tumblr blog/custom domain setup and I loves me some bandwagon!

## But what does it all mean, Basil?

Once I refocused on the original point of blog.php, it all became clear.  The point wasn't to write a CMS, although I did manage to delude myself into believing I would use it extensively.  *The point was to learn more about [Model-View-Controller architecture](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)*.  I think I've done that.

I realize this may seem like a betrayal of the original premise of starting a blog -- building on free land and not in the walled garden social media giants -- but the way that **tumblr** is set up, I'm positive that I'd never have to worry about losing my content as I plan on making rolling backups via RSS extraction.  That would be something new to write and would **definitely** be done in Python!
