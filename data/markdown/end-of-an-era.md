---
date:    2019-10-17
subject: End of an Era?
tags:
    - planet
    - freeloading
    - landsat-viewer
abstract: |
    May have to decommission Landsat Viewer because it looks like Planet.com doesn't
    offer ~~freeloader~~ enthusiast use of their APIs anymore. :(
---

Yesterday I wanted to see how a major road construction project near my commute
looks from the sky.  Bringing up [Landsat Viewer](https://landsat-viewer.dev.bazile.org),
I get tile errors when I actually click on one of the footprints:

![tile error](/public/writing/attachments/landsat_viewer_tile_error.png)

I looked at the backend logs and saw the tile proxying calls are failing with
`HTTP 401`.  Tried logging into [planet.com](https://planet.com) and am
immediately stopped by this message:

!["Your 14 day trial access has ended. Please contact our sales team to learn how you can continue to leverage our many solutions."](/public/writing/attachments/planet_upsell.png)

Still trying to scratch the "what does this construction site look like from the
sky" itch, I looked for their old public-access Planet Explorer UI but can't even
find _that_.  It looks like at some point over the last few months, Planet has
gone full-commercial.

To be fair, I was using their developer/enthusiast access level which had a data
usage cap as its only restriction.  I'd probably have to pay out of pocket (a
price that cannot be known without talking to Sales so I'm guessing it's well
beyond an individual's reach) since I don't think that "rando with massively
underpowered webapp that shows Landsat data" qualifies under their
Educational/Research license terms.

Maybe I should ask them if we low-cap freeloaders are still supported...  It's
either that or figure out how to orthorectify and tile the official thumbnails... 🤔
