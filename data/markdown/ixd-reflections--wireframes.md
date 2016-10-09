Date:     2016-05-30
Subject:  Interaction Design Reflections: Wireframes
Tags:     interaction design, ux, school, coursework
Abstract: This week, we performed an iterative wireframe exercise in order to flesh out the navigation architecture for our imaginary mobile app.

## Sketch first, ask questions later

We did sketches with plain old pen and paper, then posted them to a student group forum for peer review.

[![ehrmagerd dat handwriting](../writing/attachments/coursework-wireframe-chickenscratch.jpg)](../static/uxd_coursework/61095-interaction-design-app-wireframes/Sketches Round 1/)

Despite my atrocious chickenscratch, I received generally positive feedback with a few suggestions identifying conceptual problems related to the lower navigation bar.

### Navigation elements interfere with discrete activities

> On your “Account” wireframe, do you think that the tray navigation
> is necessary there? Could it distract the user from adding funds
> and potentially have them abandon and not make a payment?

Here was the first major problem.  The activities _Add Account_, _Add Funds to Account_ and _Add Payment Method_ are all discrete activities with definitive outcomes (e.g., _Save_ or _Cancel_, _Remove_ or _Cancel_, etc), but I had kept navigation elements (i.e., lower tab bar and the _&lgt; Back_ buttons) present on those screens.  At best, those components _only_ clutter up the UI; at worst, they'd present huge vectors for user error and confusion.

I went with the suggestion of [modalizing](https://en.wikipedia.org/wiki/Modal_window) (probably not a word) those activities.

### Top-level navigation elements to activities that will not be used often

> ADD ACCOUNT: Again I think the process here is good, but it should
> not be part of the main nav because once your kids are entered you
> will have no further use for it.

This one actually made me laugh once I thought about it.  Here's this button that you will literally _never_ need again if you've only got the one child in school __right there at the bottom of the app__.  Ever-present.  Mocking you. _Judging you_.  All because you can never use it again.

I fixed this one by restructuring the architecture around three key areas: _Home_, _Accounts_ and _Payment Methods_.  Incidentally, those ended up being the three navigation buttons on the lower nav.


## The Takeaway

### Spent _a lot_ of time with [proto.io](https://proto.io) this weekend

Because last week led up to a holiday, the schedule was relatively light&mdash;I was actually able to play around with proto.io this time.  As it turns out, it's pretty frickin sweet.  Who knew?

[![proto.io example](../writing/attachments/proto-dot-io-example.gif)](https://proto.io/en/demos/)

> My crappy screenshots that don't really do it justice...

You can create an interactive prototype (composing transitions, state changes, animations, etc.) that responds to user inputs and covers most major mobile interface design languages (e.g., iOS, Material Design, etc).  It's not unlike XCode's Storyboard functionality except cross-platform and without the [$1300](http://www.apple.com/macbook/) cover charge.


### Proto.io does have its flaws

Granted, there are some quirks about the interface that bug me.  For example, double-clicking on an element that contains text won't actually select the text inside of it.  The required interaction is:

1. Double click element.
2. Wait half a second.
3. Double click again.
4. Crap, didn't work.  Pause for another half second.
5. Double click.
6. Still nothing.
7. Click furiously until _something_ happens.

Also, if you turn off _Snap to grid_ (because it's just too damn aggressive), <kbd>Shift</kbd>+<kbd>Up|Down|Left|Right</kbd> will shift selected elements by `Infinity`.  Let that percolate in your mind for a moment...

But considering the functionality packed into it, I'm inclined to just live with those complaints.


## Attachments

[<img src="../writing/attachments/coursework-IxD-Wireframes-icon.png" alt="PDF" style="width: 100px !important; box-shadow: none !important; border-radius: 0 !important;"/>](//coursework.andsoitcontinues.com/61095-interaction-design-app-wireframes/deliverable.pdf)

