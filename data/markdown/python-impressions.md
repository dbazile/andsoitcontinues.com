---
date:    2013-08-05
subject: Python Impressions
tags:
    - python
    - php
    - complaining
abstract: |
    Coming from PHP, I've found a few differences between the way I
    like doing things and [The Python Way](http://www.python.org/dev/peps/pep-0008/)
    that are seriously challenging my assumptions.  Some I like, some
    I don't, and some I'm just plain old conflicted about.
---

I'll skip the cheerleading session by just listing the negatives.

*Disclaimer:  I have a habit of making sweeping generalizations that are probably not universally true -- this effect is magnified when discussing things that are new to me.*

## Capitalization and Naming Conventions

So the Python style guide promotes the following naming convention:

```python
class SomeClass:

    def some_method_that_does_something(self, other_item):
        some_variable = other_item.do_something()
        return some_variable
```

This is troubling for me since I'm solidly in the "camel case" camp.  As a user of multiple programming languages and an advocate for making code as descriptive as possible, I give my variables meaningful names such as `numberOfRecords` or `distanceFromCenter`.

From an ergonomic perspective, the equivalent of these, `number_of_records` and `distance_from_center` takes me away from my "keystroke zone" -- I have to jump top-right to grab the underscore each time I reach a word boundary.  This usually leads to more typos as on return from the voyage to the underscore key, I end up hitting the wrong key next.

From a typographical perspective, I'd argue that the use of underscores breaks up the visual silhouette a variable/function name has by introducing visual gaps which may introduce difficulty in quickly reading and comprehending long or "busy" statements, such as:

```python
take_multiple_objects_and_do_stuff(first_object_in_recordset, second_object_in_recordset, some_property)
```

Lastly, from a purely aesthetic perspective, I think underscored names give the appearance of antiquity -- like "the old way of doing things" -- such as the difference between procedural `mysql_fetch_object()` and object-oriented `$db->fetchObject()`.  A frivolous complaint to be sure, as nothing is stopping anyone from rewriting PDO with `begin_transaction()` or `set_fetch_mode()`, Python style.

As a realist, I understand that to other "normal" developers, there is probably no discernible difference to doing it one way or the other.  As an irrationally stubborn person, I will probably continue writing camel-cased code anyway, Python convention be damned.

## Namespacing via Modules

Python also presents a challenge to me when structuring modules.  I like structuring my PHP with one class per file, namespaces to group like items and provide deconfliction and, if necessary, use of classes by referencing their fully qualified names thusly:

<div class="codeblockname">./blog/models/Story.php</div>

```php
namespace blog\models;

class Story {
    private $subject;
    private $content;
}
```

<div class="codeblockname">./blog/helpers/PermalinkHelper.php</div>

```php
namespace blog\helpers;

class Helper {
    public getPermalink() {
        return 'something.html';
    }
}
```

<div class="codeblockname">./blog/index.php</div>

```php
require 'models/Story.php';
require 'helpers/PermalinkHelper.php';

use blog\models\Story;

$story = new Story()
$permalink = new blog\helpers\PermalinkHelper();
```

In Python, I haven't found the sweet spot yet.  With keeping the exact same number of files, it would look like this:

<div class="codeblockname">./blog/models/Story.py</div>

```python
class Story:

    def __init__(self):
        self.subject = None
        self.content = None
```

<div class="codeblockname">./blog/helpers/PermalinkHelper.py</div>

```python
class PermalinkHelper:

    def getPermalink(self):
        return 'something.html'
```

<div class="codeblockname">./blog/main.py</div>

```python
import models.Story.Story
import helpers.PermalinkHelper.PermalinkHelper

story = models.Story.Story()
permalink = helpers.PermalinkHelper.PermalinkHelper()
```

To me this is hideous.  I am aware of `from models import Story` but say I don't want `Story` in the main file's global namespace?  If I just wanted to be able to refer to the class by what I believe should be its fully qualified name (models.Story), I'd have to do one of the following:

+ Add an intermediate step of defining an `__init__.py` file inside of the **models** folder with `from Story import Story`
+ Create a `models.py` in the root folder and put *every single class I want nested directly under models in there*.

I'm sure that with further research, I will find an architecture that agrees with my delicate sensibilities.  The quest goes on!
