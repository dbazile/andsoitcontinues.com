---
date:    2017-10-01
subject: Outlook.com and Data Loss
tags:
    - email
    - data loss
    - griping
abstract: |
    If you're using Outlook.com to autoforward to another email
    address, turn off "delete after forwarding" and make sure it's
    not silently dropping messages.
---

## What's all this about then?

Several years ago, I migrated the family's email &amp; calendaring from GMail to Outlook.com after getting tired of Google's fast-and-loose implementations of the IMAP/CalDAV specs wreaking havoc in every email/calendar application I've ever used.  Well, at some point this year, I think Microsoft has made some configuration change that's led to the __silent, likely irrevocable loss of an unknown number of emails without any warning whatsoever without any timeline for a fix__.

What's the world coming to when you can't trust your email provider to not randomly lose things without telling you?


### Some history: lots of false-positive spam

A few months ago, I noticed that notifications from my banks (plural)--notifications that I'd been receiving just fine for the last several years, would occasionally get filed in the _Spam_ folder of my primary email address (the one Outlook is autoforwarding to).  Assuming that some heuristics filter was just temporarily confused, I just diligently marked everything _Not Spam_ and kept rolling, no big deal.

Eventually, this started happening regularly enough that I started to think _something_ was wrong.  So, I take the additional step of logging into Outlook.com and _explicitly_ mark all of my banks'notification return addresses as safe senders.

Problem solved, right?


### And then, silence

A few weeks ago, I stopped getting emails from two banks altogether.  Assuming the banks were being... well, banks (with their tradition of IT incompetence), I logged in and double-checked the notifications settings to make sure they were still on (they were).

__The only reason I even found out this was happening is because I recently requested an estimate from a local contractor who was supposed to email it to me.  After waiting a few days for it, I called and asked them to resend which they did and I _still_ didn't see it__.

By now I was already very suspicious and logged into Outlook.com to disable the "delete after autoforwarding" option and asked the contractor to resend.  __Sure enough, it shows up only at Outlook.com and never autoforwards.__


### Seriously Dave, what's the big deal?

What if a relative or an old acquaintance tried to email me?  I know _several_ people in both technical and non-technical fields that have 1000+ unread emails in their inboxes (which itself is something that drives me absolutely nuts, but I digress).  Would one of those people even notice a "Sorry, your email to Dave bounced" email from mailerdaemon or would they assume Dave's just being a friggin jerk, a flake or a bad nephew?


### First step is admitting you have a problem

Now that I knew what's happening, I observe for several days and see that 2 out of 3 messages showed up at Outlook.com and were never autoforwarded.

After scouring the entire Internet for "why 'tf won't Outlook forward my crap", wading through post after post in support forums consisting of "lol, have you tried turning it off and on again?" tier-1 phone support boilerplate BS, I stumbled upon [this MSDN blog post that _excellently_ explains what's happening without being patronizing](https://blogs.msdn.microsoft.com/tzink/2016/05/19/why-does-my-email-from-facebook-that-i-forward-from-my-outlook-com-account-get-rejected/):

> Exchange server has a feature wherein it "fixes up" content in a message. This has been around for many years and it's to prevent malformatted data from going into your mailbox where it could cause a corruption problem. So, if messages arrive in a certain way, it converts it to a format it does expect. For example:
>
> __Before being fixed:__ `Joe Sender <joesender@example.com>`
> __After being fixed:__ `"Joe Sender" <joesender@example.com>`
>
> There are good reasons for doing this, especially in enterprise environments, that I won't get into here. To a human, the message looks identical. But the problem with doing this is that if a message has a DKIM signature, then fixing up the message will break the DKIM signature - even doing something as small as adding quotes around the Display Name breaks the existing DKIM-Signature.

Which is like, "cool, they know what the problem is".  Then I looked closer at the dates on the article.

May.  2016.  With an update at the top that reads:

> Update on Jan 25, 2017 - Still no timeline on a fix for this, we have repeatedly hit issues. 🙁

WAT.


### Now what?

I filed a support ticket explaining the issue and asked for a way to resolve.

Several days later when I finally got a response, it was the expected "lol have you tried turning it off and on again?" boilerplate but by then, I'd already started migrating all of my stuff away from Outlook.com.

So I reply with this letting them know they can do whatever they want because I've already divested:

> I already contacted [the other email provider] and went through their troubleshooting procedures, then tried removing and re-adding the forward and it didn’t work.
>
> I found this MSDN blog post a few days ago which actually explains what is going wrong without assuming the user doesn’t know how email works: https://blogs.msdn.microsoft.com/tzink/2016/05/19/why-does-my-email-from-facebook-that-i-forward-from-my-outlook-com-account-get-rejected/
>
> Please understand that, regardless of what the underlying cause actually is, this is data loss of the most unacceptable kind—silent data loss. I wouldn’t have even known anything was wrong if one of the businesses I’m contacting hadn’t told me they were getting email bounces.
>
> I’ve decided to just stop using my outlook email for anything important and am in the process of migrating my stuff out of Outlook.com permanently.
>
>Thanks,
>David Bazile

No rest for the weary...
