---
date:    2014-06-17
subject: A Week With Ruby
tags:
    - ruby
    - development
abstract: |
    I test-drove Ruby for a week and have recorded my results here,
    lest I forget in six months...  At the risk of incurring the
    wrath of Rubyists everywhere, I am publishing my completely
    superficial, unrelated-to-any-objective-metric-whatsoever
    assessment of the language.
---

## Things I like about Ruby

I was a bit skeptical of the claim at first, but Ruby does live up to its credo of developer happiness.  Or maybe I just really enjoy writing new code--could go either way...


### Regular Expressions baked directly into `String`

I like not having to import extra libraries and/or generate a bunch of peripheral objects just to perform regular expressions on my strings (something I need to do more often than not).  This is one thing I really love about JavaScript and, by extension, Ruby: the regular expression engine is *right there* by the side of your dinner plate, not in the kitchen cabinet where it waits for you to assemble it each time.

```ruby
no_vowels   = some_string.gsub(/[aeiou]+/, "")
all_numbers = user_input.match(/(\d+)/)
```

### Symbols as hash keys

Although this is more of a "it looks cool" thing, I really like the concept of `:symbols`.  It makes it very obvious that whatever you are referring to is an identifier for something and not just some random string literal.

```ruby
gizmo = {
    "name" => "Gizmotron9000",
    "description" => "Its mystery is only exceeded by its power"
}
gizmo = {
    :name => "Gizmotron9000",
    :description => "Its mystery is only exceeded by its power"
}
```

In my opinion, the latter is a tiny bit more readable than the former, if for no better reason than that my text editor of choice will highlight them differently than the string literal.


### I like the REXML API, buuuuut...

I love the fact that XPath is exposed everywhere and I found the API easy to work with, but there's a point I reached that kind of freaked me out.  Refer to the following snippet:

```ruby
document = REXML::Document.new(xml_string)

# Find a single node in our structure
document.elements["//some_node"]
```

At first glance, it looks like we're accessing a dictionary to find the value whose key is `//some_node`, but we're actually executing an XPath query against a structure which is definitely **not** a dictionary.

The property `elements` on an instance of `REXML::Document` is of class `REXML::Elements`, [which is completely undocumented](http://ruby-doc.org/stdlib-1.9.3/libdoc/rexml/rdoc/REXML/Elements.html) at the time of writing.

Personally, dictionary-access syntax used to execute methods against an object just feels wrong.  This just makes it seem like there's too much going on behind the scenes that I don't know about.

This would make more sense to me:

```ruby
# Not an actual method
document.elements.find_first("//some_node")
```

## Things I dislike about Ruby

### Last line of code in a function weirdness

Consider the following contrived example:

```ruby
def foo(bar)
    # Add an element to bar hash
    bar["dave"] = "awesome"
end
```

Invoking `foo` will return `"awesome"`.  I didn't ask it to return any value--I just wanted it to add an element to a hash.  The fact that the statement that adds the element falls last in the function means that it will automatically be returned.  I know this probably isn't that big of a deal as long as you only use it when you absolutely know you want a function's return value.  But knowing that what I intended to be a void function now returns some random value doesn't sit well.

Your function could return anything whether you want it to or not.  I'm not comfortable with implicit returns.  Which relates directly into the other thing I don't like:


### No `()` security blanket

Maybe it's the residual effect from using Python 3 for a while, but I've now associated all function calls with parentheses and any function call that doesn't conform to that makes me nervous.

```ruby
foo = some_object.something
some_object.something_else
```

Am I invoking some method on an object or am I peeking at a property?  It could go either way.  Even if the item has a definitive verb for a name, I have no idea just looking at the code.


### Namespaces?

I believe Modules are supposed to facilitate namespaces.  It's a silly complaint for sure, but I'm not a fan of `::` notation.

```ruby
require './helpers/file/html/LinkScraper'
link_scraper = Helpers::File::HTML::LinkScraper.new
```


### Multi-line comments

I think the multi-line comments were put in specifically as punishment to anyone who likes to document their code in the source.  Observe:

```ruby
=begin
Here's my docstring

@param string foo
@param string bar
=end
```

In addition to being an absolute eyesore what with using equals in its open and close, it also has to occur at line position 0 or it's considered an error.


## Conclusion

All in all, I did have fun test driving the language.  I definitely wouldn't have any doubts about potentially supporting a Ruby on Rails application if the opportunity ever presented itself.  That said, I think Python will remain my preferred personal scripting language for the time being. :)
