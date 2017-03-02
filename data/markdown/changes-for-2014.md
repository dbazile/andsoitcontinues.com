---
date:    2014-01-11
subject: Changes for 2014
tags:
    - could you spare some change
abstract: |
    Definitely definitely not a New Years Resolution list.  I've made
    a few changes to my workflow for this year.  This is my attempt at
    documenting those changes and their effects.
---

> Somebody once asked could I spare some change for gas<br />
> I need to get myself away from this place<br />
> I said yep, what a concept; I could use a little fuel myself<br />
> And we could all use a little change<br />
> <span class="quoth">Smash Mouth, "[All Star](http://en.wikipedia.org/wiki/All_Star_(song))"</span>

## I have moved to `the_land_of_snake_case`

I may have crossed over to the dark side on this one.  I have adopted snake-case (e.g., `do_something(text_data)` versus `doSomething(textData)`) as my default scripting name convention.

### How did this happen?

After [several earlier grumblings about snake-case](python_impressions.html), I figured I should just try it out and try to deem if my complaints were justified.  I tend to write very short statements, such as the following contrived example:

```python
def do_something_complex(raw_dough):
	sweetened_substance       = add_sugar_to(raw_dough)
    flattened_sweet_substance = flatten_object(sweetened_substance)
    raw_pancake               = make_round(flattened_sweet_substance)

    return put_on_the_griddle(raw_pancake)
```

As opposed to this equally contrived example:

```python
def do_something_complex(raw_dough):
	return put_on_the_griddle(make_round(flatten_object(add_sugar_to(raw_dough))))
```

Because I write such short statements (that fly in the face of the whole "state is bad" functional programming ethos), I have not run into the "underscore overload" problem I originally complained about.  I haven't looked at that many other people's code though, so my mileage may yet vary...

That said, I am reserving this convention for Python and PHP, as that's where people would tend to see snake-case.  JavaScript, maybe not so much.  It's much more common in my work to see people using camel case in their JS.

Now the next adventure is adjusting to the C#/.NET naming convention `Where` `Everything` `You` `Do` `Is` `In` `TitleCase`.

## I went ahead and wrote a Blog Engine anyway

Left tumblr.  I'm now rendering static HTML from markdown sources (doesn't that just seem to be the *in* thing these days?).

### Performance changes

Shaved 300 KB (300%) and a ton of 3rd party code off of the page.  The page size doesn't matter as much, since this is hardly a high-traffic website.

### Superficial changes

Refreshed the graphics for this year, leveraging some of the visual patterns I saw while on vacation this Christmas.  I was going for slight organic with some connotation of "ongoing-ness".

I also tightened up the typography of the page by introducing a new font and implementing some of the techniques I've learned over the last few weeks.

## I finally bought a New Computer

I am finally rid of the chain gang.  With the arrival of my [Lenovo ThinkPad T440s](http://shop.lenovo.com/us/en/laptops/thinkpad/t-series/t440s/), the Dell Inspiron 1300 with its 7 minute battery has been retired officially.  I am mobile again!

### New capabilities

With a larger screen, better keyboard, tons of memory and decent processor speed, I am actually able to run the latest versions of software including Visual Studio 2013, Photoshop CS6.  With a renewed sense of inspiration and confidence in my tools and the ability to work from anywhere again, I plan on doing much more personal design and development this year.
