Date:     2016-06-13
Subject:  Interaction Design Reflections: Interactive Prototypes (Redux)
Tags:     interaction design, ux, school, coursework
Abstract: This week, we refine the prototypes we built last week based on peer feedback.

## Putting the "iterative" in "interactive"

Get it?  Because one word is a subset of the other!  <small>...I'll let myself out...</small>

Based on the feedback I got from my peer group last week, I noted and attempted to correct a number of deficiencies.

__TL;DR__, I'll spare you the boring details and offer the link to the updated version up front:

[![new and improved(?)](../writing/attachments/screenshot-interactive-wireframe.png)](https://davidbazile.proto.io/share/?id=65379e6f-6bbb-4c26-a598-d704d4690ced&v=4)


### Users need more information regarding auto-refill (how often does it occur, how much is refilled, is there a balance trigger, etc)

<img
    src="../writing/attachments/coursework-ixd-prototype-autorefill-animation.gif"
    alt="fix for auto-refill ambiguity"
    style="width: 200px; float: right; margin: 0 0 1em 1em;"/> I addressed this by adding a more descriptive label to the toggle button that reveals a trigger balance field beneath it:

The initial value for that field should ideally be rounded to the current balance of the account as a convenience.

My intent here was to keep the "simple" path clean for the non-technical persona (who just wants to open the app, add funds and not be bothered by anything else), while providing enhanced options for interested parties.

### Users have no way to view a list of things they've "favorited"

<img
    src="../writing/attachments/coursework-ixd-prototype-favorites-animation.gif"
    alt="fix for missing favorites list"
    style="width: 200px; float: left; margin: 0 1em 1em 0;"/> This I solved by just adding another screen since it'd be pretty hard to piggy back this onto something else.

This view lists everything the user has "favorited" (which, according to Oxford, [_is_ a verb](http://www.oxforddictionaries.com/definition/english/favourite)) and affords the ability to "unfavorite" (which sadly, as of 2016-06-13, [hasn't yet made the cut](https://web.archive.org/web/20160614001446/http://www.oxforddictionaries.com/us/definition/american_english/unfavourite?q=unfavorite).

And even better, it doesn't obstruct the "simple" path my non-technical persona needs while at the same time providing an enhanced experience for interested parties.
