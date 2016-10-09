Date:      2015-09-05
Subject:   Three Cheers for Python
Tags:      python, drinking the koolaid, code, github, rdf
Abstract:  I am solidly a Python fan.  There, I said it.

## Conversion Complete

I'm drinking the koolaid.  I've resigned myself to the fact that the docs are borderline horrendous.  I know enough about the package/module infrastructure that I've stopped wishing horrible things happen to its designers.  I've learned my way around `pdb` instead of dropping `print(); exit()`s everywhere.  I've watched many awesome talks from _PyCon 2015_ on YouTube, including:

1. David Beazley's [whirlwind tour of the module and package system](https://www.youtube.com/watch?v=0oTh1CXRaQ0) (a 3 hour doozy, but well worth it)
2. Miguel Grinberg's [talk about RESTful API design](https://www.youtube.com/watch?v=pZYRC8IbCwk):
3. Raymond Hettinger's [talk about dependency injection via Python's object inheritance pattern](https://www.youtube.com/watch?v=EiOglTERPEo) (which is frickin awesome; if you watch no other video, check _this_ one out)
4. Raymond Hettinger's [talk about PEP8's shortfalls IRT writing intelligible code](https://www.youtube.com/watch?v=wf-BqAjZb8M)


## Some recent utility scripts I've written

As usual, a problem arises during the day and much code is slung to solve it.  Here are two tiny artifacts of those efforts.

### scraper.py: An RSS Scraper

Not bulletproof, but it gets the job done for the most part.  I had to implement my own HTML parser because I wanted to keep it down to _just_ the standard library and no third party packages.  That parsing algorithm is about as naive as a newborn baby, so don't expect magic and definitely don't try to build an Instapaper around it.

[@dbazile/scraper.py](https://github.com/dbazile/scraper.py)

### compile_greenturtle_from_github.py: The most ridiculous Ant clone ever

Those of you not in the know, [Green Turtle](https://github.com/alexmilowski/green-turtle) is a client-side [RDFa](http://www.w3.org/TR/rdfa-primer/) processor library that I'm using for something we're building at work.  Unfortunately, the guy who wrote it used [Apache Ant](http://ant.apache.org) as the build task runner.  In defense of the creator, it was first built a few years ago and I know as well as the next developer how much intertia there is in deciding to move from one build process to another.

After coaching our intern through hand-concatenating the files the first time for the sake of expedience (it was either that or go through the rigmarole of installing the JRE and all the other bits and pieces), I realized that wasn't a sustainable solution.  So I did some hardcode yak shaving and wrote this up.

This thing will fetch all the pieces defined by the build manifest, automatically concatenate them and wrap them in a bootleg AMD wrapper for your convenience.

[@dbazile/compile_greenturtle_from_github.py](https://gist.github.com/dbazile/92d2f889c9ba3df87cf8)
