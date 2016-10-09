Date:     2015-03-22
Subject:  Usability Reflections: Designing a Remote Usability Test
Tags:     usability, ux, school, coursework
Abstract: This week, we were tasked with designing an actual remote usability test with Loop11 and running real people through it.

## What is Loop11?

[Loop11](http://www.loop11.com) is a service that lets you design, execute and analyze remote usability tests.

### How does it work?

I snuck a peek at the source code for the actual test pages, and it seems to work as a proxy&mdash;the page under test is returned from their servers, resource URLs are rewritten from relative to absolute and page URLs are rewritten to use their server as a gateway.  This way, they can intercept page navigations and plot the path a user takes through your site for any given task on your test.  Pretty <strike>scary</strike> slick, no?

### What does it look like?

<svg viewBox="0 0 100 60" style="width: 100%; background-color: #555; cursor: default;">
  <rect x="2" y="2" width="96" height="10" fill="#0b5" />
  <rect x="2" y="12" width="96" height="46" fill="#eee" />
  <g fill="white" font-size="3" style="font-family: Helvetica Neue, sans-serif">
    <text x="4" y="6">You are planning a birthday party.  Find a</text>
    <text x="4" y="9">5-star birthday cake recipe.</text>
  </g>
  <g fill="rgba(0,0,0,0.2)">
    <rect x="65" y="5" width="15" height="6"/>
    <rect x="82" y="5" width="15" height="6"/>
  </g>
  <g fill="#eee">
    <rect x="64" y="4" width="15" height="6"/>
    <rect x="81" y="4" width="15" height="6"/>
  </g>
  <g fill="rgba(0,0,0,0.1)">
    <rect x="5" y="15" width="22" height="22"/>
    <rect x="5" y="40" width="20" height="2"/>
    <rect x="5" y="45" width="17" height="2"/>
    <rect x="5" y="50" width="22" height="2"/>
    <rect x="34" y="15" width="61" height="12"/>
    <rect x="34" y="30" width="12" height="2"/>
    <rect x="34" y="35" width="10" height="2"/>
    <rect x="34" y="40" width="16" height="2"/>
    <rect x="55" y="30" width="12" height="2"/>
    <rect x="55" y="35" width="10" height="2"/>
    <rect x="55" y="40" width="16" height="2"/>
    <rect x="76" y="30" width="12" height="2"/>
    <rect x="76" y="35" width="10" height="2"/>
    <rect x="76" y="40" width="16" height="2"/>
    <rect x="34" y="47" width="29" height="11"/>
    <rect x="66" y="47" width="29" height="2"/>
    <rect x="66" y="52" width="20" height="2"/>
    <rect x="66" y="57" width="25" height="1"/>
  </g>
  <text x="50" y="35" fill="#555" text-anchor="middle" font-size="7">Participant's View</text>
</svg>

Loop11 places a toolbar at the top of each page to act as the moderator.  The toolbar lets the user know their progress through the test, what task they are on, what the task requires and lets them announce completion or abandonment of that task.


## Building the Test

A Loop11 test is an arbitrarily-ordered queue of two basic constructs: *Task* and *Question*.  You can add things to the queue, reorder, edit or remove them at any time.

### Tasks

A task can be described as follows:

> Starting from URL `X`, do activity `Y` and if you end up on URL `Z[]`, it's a success (anything else is considered a failure)

`X` is the particular page on the site you are trying to test.

`Y` is the scenario and instructions, which will be displayed at the top of the window while the user is attempting a task.

`Z[]` can be a set of as many URLs as you'd like&mdash;useful if there are more than one path to completing the task successfully.  Any navigation outside of one of the URLs in `Z[]` counts as a failure.

### Questions

Loop11's Questions come in a **huge** variety of styles in presentation and in response.  I barely scratched the surface, using only the following:

* Single choice (radio buttons)
* Multiple choice (checkboxes)
* Likert Scales
* Open-ended (free text)


## The Takeaway

Once I learned their UI, I was able to build the test via the composition of a flexible set of components.  At any point in the test design, I was able to preview the individual component I was working on or the entire test as a whole.

### Technical issues

I *did* run into some minor technical problems due to the proxying Loop11 does.  Google Maps doesn't like hostnames using API keys that don't match and will complain about it **very** noisily (in the form of alert boxes on every page).

Thankfully, since I didn't base any of my tasks on the map interactions, it was more of an annoyance than a show stopper.



## Addendum: Tasks &amp; Questions

The site under test was [Weather Underground](http://www.wunderground.com).

### Tasks & Verification Questions

1. You are planning a hiking/camping trip at Shenandoah National Park in Virginia for next week Monday-Wednesday. Will you experience any inclement weather (e.g., thunderstorms, snow, heavy winds, etc)?
  * Which of the following types of weather are predicted to occur on your camping trip?
  * How easy was it to find the information you needed to answer that question?

2. You want to visit Denali National Park in Alaska but don't want to freeze to death. Which months have average lows _above_ 20°F?
  * Which months have an average low of _higher_ than 20°F?
  * How easy was it to find the average low temperature?

3. Can you find the page on the website that has data on hurricanes & tropical cyclones?
  * How easy was it to find the link to the Hurricanes & Tropical Cyclones page?

4. You are doing research on Hurricane Sandy. Can you find a map showing the path the storm travelled, from the time it formed to the time it made landfall?
  * How easy was it to find the link to the map of the path Hurricane Sandy took?

5. You want to track Tropical Cyclone Nathan, an active storm. Can you find the map showing TC Nathan's predicted path?
  * Which country is the storm over now?
  * Which country is the storm predicted to be over on Tuesday 24-March?

### Follow-up Questions

1. Were any of the tasks hard to understand?
2. Did you run into any technical problems when trying to do the tasks?
3. What is your opinion on the amount of information shown on the Forecast page?
4. How likely are you to use Weather Underground in the future to Forecasts?
5. What is your opinion on the amount of information shown on the Weather History page?
6. How likely are you to use Weather Underground in the future to view Historical Weather Data?
7. What is your opinion on the amount of information shown on the Hurricane & Tropical Cyclones page?
8. How likely are you to use Weather Underground in the future to track and research Hurricanes and Tropical Cyclones?
9. Please rate your satisfaction with the following pages (measured in Likert scale):
  * Weather Forecast Page
  * Historical Records Page
  * Hurricane and Tropical Cyclone Page
