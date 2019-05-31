---
date:    2015-12-03
subject: Defending Function Hoisting in a Commit Message
tags:
    - javascript
    - style
    - readable code
    - hoisting
    - politics
    - eslint
abstract: |
    I recently had to defend the disabling of code style enforcement
    to allow function hoisting.  Knowing that I wouldn't get away with
    such a unilateral change without a _very_ good reason, I wrote a
    lengthy justification in my commit message.
---

## Background

So I work with some awesomely [_Smart and Gets Things Done_](http://www.joelonsoftware.com/articles/GuerrillaInterviewing3.html) kind of engineers.  I've learned more over the last six months than I did working for my previous employer for two years.  As should be expected in any healthy organization, there exists a diversity of experience and of opinion on my team.  Several of my fellow developers have a preference for using function expressions over named function declarations, e.g.:

```javascript
let add = (a, b) => {
  // Do something
};
var subtract = function(a, b) {
  // Do something
};
```

### Imma have opinions now, kay?

This is a purely subjective argument but I dislike this style.  To me it looks like a misappropriation of variable assignment.  Absent syntax highlighting (e.g., when viewing code in a low-powered text editor), you're scanning the left-side of the text editor to see what's coming up and you see a variable declaration.  But wait, you didn't look far enough to the right to see that it's actually a function.

In the weeks leading up to the ES2015 spec being finalized, I started seeing this kind of code popping up all over the web in tutorials and "first looks" and it drove me batty:

![goddammitwhy?!](/public/writing/attachments/goddammitwhy@2x.png)

Maybe it's my own background---I cut my teeth on PHP, moving onto Java before I _really_ started focusing on JavaScript.  PHP and Java are pretty darn clear about what constitutes a function/method.  Granted you _could_ do this, but then you should have someone take your keyboard away:

```php
$add = function($a, $b) {
  // lolwut
};
$subtract = function($a, $b) {
  // lolwut
};
```

But, I digress!  To each his own, right?


### Enter ESLint

So up until a few months ago, we were using [JSCS](http://jscs.info) and [JSHint](http://jshint.com) to enforce code style and quality.  When the final ES2015 spec was announced, we started using a lot more of the new syntactical sugar, which resulted in [tooling breakage left and right](https://github.com/jshint/jshint/issues/2746).  Every time we'd try to use some new language feature, the console would bark at us that something was wrong.

We eventually opted to switch to [ESLint](http://eslint.org), which was doing a much better job of keeping up to spec _and_ would let us combine our style and error checking into one package.

### In the changing of the guard, something was lost

Because we have a lot of code, we split the work to convert everything over to use ESLint, enabling one rule at a time until we finished.  I was not the one to turn on the `no-use-before-define` rule and so all of my previous code was reorganized to comply with "thou shalt define _the universe_ before thou speakest to me of anything".

We're an Ember shop and Ember does things in a very class-oriented way, so I wouldn't notice this change for a while.  I finally bumped into this new unpleasant rule when writing a new utility module and this kept getting flagged:

```javascript
export function performComplicatedOperation(input) {
  const {important} = _doSomeSpecificThing(input);  // <-- lint error
  return important;
}

function _doSomeSpecificThing(inputA) { ... }
```

Knowing that I've written other modules in the codebase that follow this pattern, I opened up one of my larger modules.  To my absolute horror, I saw that what was once a thing of (relative) beauty was turned __completely upside down__.  Helper methods dominate the module---I had to scroll down for several hundred lines before I found the external API.

<img
    src="/public/writing/attachments/upsidedownland@1x.png"
    style="display: block; width: 350px; margin: 0 auto;"/>

Needing to get a feature implemented and not wanting to have to lose momentum by stopping to research, then politick for hours just to get that rule squashed, I just dropped an `/* eslint no-use-before-define: [2, "nofunc"] */` override at the top of the file and kept working.

So, this week, I had the time to do that research and took care of the rule myself.


## There's a point down here somewhere, let me try to find it...

Now, _I_ know why I use function declarations and why I order my functions a certain way.  But I'm always wary to directly confront other developers about their particular coding styles, lest I spark a flame war that burns for a thousand years.

### Research: digging into the past

I searched the repository history for previous commits that still had the .jscsrc and .jshintrc files.  I copied those back into the project directory and then ran `jshint` and `jscs` on my code to make sure that I was actually making a true assertion by saying that we weren't enforcing that "define it before you call it" rule before.

```javascript
{
    ...
    "latedef": false,
    ...
}
```

> Yep, there it is.

So I figured the best bet would be a single easily-reverted commit that changes the rule and removes my inline overrides in the code I'd written since then, paired with a commit message that contains a (relatively) exhaustive list of reasons for keeping the rule change and several quotes from respected voices in the development community.


### Politicking: the Commit Message

I didn't _intend_ to get meta with this post, but call it a happy accident that the most important part of the post is at the very bottom _after_ all of the implementation details have been written.

Without further ado, that commit message is below:

```no-highlight
Ease hinting rules around function declarations

OVERVIEW

The `no-use-before-define` rule here has been modified to bring it
back in line with what we had before to support the following
scenario:

    // Disallowed
    alert(lorem);
    var lorem = 1;

    // Allowed
    ipsum();
    function ipsum() {
      ...
    }

[<links to old .jshintrc and .jscsrc files in repo>]


JUSTIFICATION

This is an example of one of those rules that boils down to a
developer's personal preference, which I believe the team resolved
to leave up to individual discretion when we were building the JSCS
configuration last year--the sentiment was that we didn't strictly
_need_ to enforce one way over the other.

Function declaration hoisting allows us to hide relatively
unimportant implementation details so that the most important
aspects of a particular module is presented as the first thing you
see when you open the file.

An example of this is the CMT module, which has around 15 helper
functions that perform some small chunk of operations as delegated
by the external API. Consider what is the most important thing to
see when opening this file: the ~200 lines of string munging and
promise wrangling or the external API?

This pattern is encouraged by prominent voices in the software
development community.

Robert C. Martin, author of Clean Code, wrote:

    Vertical Ordering

    In general we want function call dependencies to point in the
    downward direction. That is, a function that is called should be
    below a function that does the calling.  This creates a nice flow
    down the source code module from high level to low level.

    As in newspaper articles, we expect the most important concepts
    to come first, and we expect them to be expressed with the
    __least amount of polluting detail__. We expect the low-level
    details to come last. __This allows us to skim source files,
    getting the gist from the first few functions, without having
    to immerse ourselves in the details.__

Granted, he was speaking in the context of Java but the principle
itself transcends specific languages.

John Papa wrote about using hoisting to make code easier for humans
to navigate (http://www.johnpapa.net/angular-function-declarations-
function-expressions-and-readable-code/):

    When I open this file __I have to start scrolling like mad to
    find out what features I can access__. So let's do that and
    scroll past this code.

    [...after ~100 lines of scrolling through code...]

    Ah, here we are. Now at the bottom we can see the features I can
    call: `getAvengersCast()`, `getAvengersCount()`,
    `getAvengers()`, and `ready()`. But if that's all I wanted to
    know, and often it is, wouldn't it be nice to put that right at
    the top? That would make it __easier for me to get in and out of
    the file quickly with what I need and not get distracted with
    all of the implementation details__.

Raymond Hettinger gave a talk about when formatting rules make code
worse (https://youtu.be/wf-BqAjZb8M?t=8m39s -- relevant portions
8:39 ~ 13:00), calls it a distraction from code quality--that by
focusing only on absolute compliance to some arbitrary code spec
over a more nuanced approach, "you end up with code that's
beautiful, but bad."

    When you start to put PEP8 at the forefront of It causes you to
    reach for something that doesn't improve code quality in an
    important way.

Again, this is in reference to Python, but the principle transcends
specific languages.

Consider "workarounds" to this limitation, __all of which are 100%
compliant with our current eslint configuration__:

 * Extract each one of those helper functions into its own module and
   chain the imports; that way, they won't obscure the external API.

 * Declare all of my helper functions inside of the external API
   functions so I can order things however I want.

 * Create some wrapper object with a late initialization and stuff
   all of the functions in there.

 * Don't extract logic into smaller functions at all; just leave it
   all inside of the external API, DRYness be damned.

All of these are compliant with the current rules, but none of them
will make the code easier to read or reason about.
```
