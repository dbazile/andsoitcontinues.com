---
date:    2014-06-19
subject: Objective-C Revisited
tags:
    - objective-c
    - ios
    - xcode
abstract: |
    A period of downtime on my current project has freed some mental
    energy which I decided to use by learning Objective-C.  My first
    exposure to the language was several years ago after which I
    reeled in horror from its syntax, thinking the only reason people
    put up with it is for a chance to win the App Store lottery
    jackpot.
---

One of the perks of working for my company is that it's big enough to have partnerships with all sorts of other companies.  One of those partnerships hooks up employees with free access to hundreds of software engineering books.  Another hooks us up free access to various online programming courses.

Digging through the available course listing, I didn't see anything that I was really dying to learn.  They did have iOS and Objective-C on the list and I figured what the heck, why not.  I have the time, they have the goods.

I'm *very* glad I did that now.


## Second Impressions

After working through the Obj-C primer, I began to feel a lot more comfortable in the language.  Some of the notation looks absolutely insane, but as with most things in life, you end up getting used to how many `*`'s and `@`'s are plastered all over the place.  Couple the warm-fuzzy attained via learning along with the fact that I am getting closer to being able to write a functioning app in what had previously seemed such an impenetrable syntax, I pressed on through lesson after lesson, relishing the little "hooray, it compiled" screens.


### Method invocation does take a while to get used to

It *is* bracket soup, but I now that I know what things actually mean, I am not completely floored when I see something like:

```objectivec
UIViewController *fooViewController = [[UIViewController alloc] init];
[self.navigationController
    pushViewController:fooViewController
              animated:YES];
```

Is functionally identical to the following Java method invocation:

```java
UIViewController fooViewController = new UIViewController();
this.navigationController.pushViewController(fooViewController, true);

// Where the method signature looks like this:

// public void pushViewController(UIViewController vc, boolean animated)
// { ... }
```

As a text formatting geek, I have to admit, aligning the colons for multi-argument messages across multiple lines does have a very satisfying feeling to it 	.

I'm still at the *Shu* stage of this process, as Alistair Cockburn would say, where it takes a second for me to grok what the heck is going on in a particular method, but that will improve with more exposure.


### Naming oddness

`@protocol`'s `@interface`'s and `@implementation`'s, oh my!  I'm assuming this is an artifact of what I've heard described as the Standardization Effect:  given two particular ways of doing things, as soon as one of them becomes adopted as the standard, the odd-man out is left with something which was perfectly acceptable a few months/years prior, but now looks completely esoteric.

I'm also a bit dubious about the term "sending a message to the object".  Why don't we make it an offer it can't refuse while we're at it. ;)


### Inheritance is sorta familiar lookin'

The inheritance mechanism is like a bit of Python in that it's doing strange things with `self`.  Difference being that Python constructors pass in `self` as an arg and this snippet returns it as an object.

```objectivec
@implementation Person

- (id) init
{
    self = [super init];
    if (self) {
        self.firstName = @"Joe"
        self.lastName  = @"Schmoe";
        self.age       = @30;
    }
    return self;
}

@end
```


## What's next

I've already found the perfect follow-on companion book to continue my educational journey into the land of iOS app development.  I'm going to attempt to build an actual application for the wife and kids.  Maybe something goofy with SpriteKit.  Nothing like having a captive audience to provide instantaneous in-person feedback. :)

I also like [what I see so far](http://www.slideshare.net/giordano/a-swift-introduction-to-swift) in [Swift](https://developer.apple.com/swift/) and I can't wait to pick it up and start messing around with it.  That's after I reach a comfortable stopping point with Obj-C, though, naturally.
