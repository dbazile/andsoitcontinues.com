Date:     2013-12-05
Subject:  SOAP Opera
Tags:     xml, php, document object model, soap
Abstract: The following is an account of my adventures in manually parsing SOAP server responses without actually using SOAP.

> XML is like violence: if it doesn't solve your problem, you're not using enough of it.
> <span class="quoth">xmlicious via <a href="http://thedailywtf.com/Comments/Oh,-XML.aspx#192304">thedailywtf</a></span>

## Background

So, at work I'm rewriting several data feed ingestion scripts from Perl to PHP, the majority of which contact remote servers via SOAP Web Services.  The problem is that while some of those web services return data that is pristine and concise, others are less than stellar.  Some contain namespaces and type definitions that yield a very predictable and well-defined data structure (i.e., arrays will appear where they should, whether only one element is there or ten).  Others seem to just be random, arbitrary and of questionable value.

Anyway, I am making good progress towards my goal and have a significant number of scripts converted.  Then I stumble upon a webservice whose authors have decided that they need to use upwards of 11 namespaces, that *everything* should be namespaced and that elements should contain children and attributes all of different namespaces.  It doesn't appear to add any value, structure or predictability to the overall data set.  Normally, nobody should ever have to worry about seeing this since SoapClient handles all of the unmarshalling anyway.  That was not to be the case this time.

## WSDL Shmisdle

So, I point my SoapClient at their WSDL and attempt a pull.  I get a SOAP-ERROR complaining about not being able to load remote schema files (I forget the specific verbiage).  I look at the WSDL and sure enough, there are tags pointing to several `http://127.0.0.1:8080/some/path/to/file.xsd` schema files.  Obviously, we don't have those files because this is a remote web service, not our own.

One option is to pull the WSDL on each request, do a regular expression to change `127.0.0.1` to their domain, cache the file somewhere, then feed it to SoapClient hoping the URI is correct and won't change.  Not a fan of this since (a) I don't want to be dealing with any more XML than I need to, and (b) I have no idea how deep this error goes and have no desire to find out.  Would I have to fix the .XSD files the WSDL is pointing to if they are also broken?  No, please.

I then take a look at what the old script was doing.  Naturally, it's building a stringified SOAP Request and firing it off using Perl's `LWP::UserAgent`...  *le sigh*.

## Life in a post-SOAP world

So, following in the footsteps of my predecessors, I string up this SOAP request manually, fire it off via CURL and get my XML string response.  Take the response string, pass it to `simplexml_load_string()` and `print_r()` the results, which was:

    SimpleXMLElement Object
        (
        )

Oh, a completely empty node.  WAT.

So as it turns out, SimpleXML (rightly) will hide anything namespaced at the current element and below.  Since the `<soap:Envelope>` node (i.e., the topmost node) of a SOAP response is namespaced, it and its children (i.e., everything we actually need) are hidden by default.  Not a problem -- we can just register the **soap** namespace and `$xml->xpath('soap:Body/getFooBarResponse')`.  This works to get the body node, but since everything inside our current data response is a big bowl of namespace spaghetti with interwoven namespaces serving no apparent purpose other than obfuscation, we'd need to know every node where the namespace changes and account for that with the proper "peek" operation.  With 4 different end points we need to hit for this particular web service, this could potentially be 4 * N special cases that need to be hardcoded into the script.  Further, this completely breaks the data adapter class we have in place for all other data sources, which assumes it's getting an object with a clean tree structure.

## A Workaround

I did a bit more research at home and came up with this superhack of a workaround:

```php
$namespaces = [
    'soap' => 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns1' => 'com.andsoitcontinues.someentity',
    'ns2' => 'com.andsoitcontinues.someotherentity',
];

$dom = new DOMDocument();
$dom->loadXml($xml_string);

kill_the_namespaces($dom->childNodes, $namespaces);

function kill_the_namespaces(DOMNodeList $node_list, array $namespaces) {

    foreach ($node_list as $current_node) {
        if ($current_node instanceof DOMElement) {
            if ($current_node->hasChildNodes())
                kill_the_namespaces($current_node->childNodes, $namespaces);

            foreach ($namespaces as $local_name => $uri) {
                $current_node->removeAttributeNS($uri, $local_name);
            }
        }
    }
}
```

## Potential issues with this workaround

I'm well aware of the potential issues, which would include:

### 1. Sibling nodes with the same name will become an array

I am a firm believer in defensive programming, so I dereference all values from any SimpleXML structure using `strval()`, `intval()` or whatever data type I'm expecting.  Invoking one of those methods on the **foo** property will yield the first element of the array anyway, which (should?) be okay for our purposes.

#### Before:

```xml
<ns1:foo>alpha</ns1:foo>
<ns2:foo>bravo</ns2:foo>
<ns3:foo>charlie</ns3:foo>
```

#### After:

```xml
<foo>alpha</foo>
<foo>bravo</foo>
<foo>charlie</foo>
```

#### Which SimpleXML will parse as:

    [foo] => Array
        (
            [0] => alpha
            [1] => bravo
            [2] => charlie
        )

### 2. Clobbered attributes with bias toward descendants

This one is a bit more serious than the aforementioned risk in that if it did happen, it would mask itself fairly well.  I don't foresee this being a huge issue for our current use case.

#### Before:

```xml
<foo ns1:somenum="111" ns2:somenum="222" ns3:somenum="333"/>
```

#### After:

```xml
<foo somenum="111" somenum="222" somenum="333"/>
```

#### Which SimpleXML will parse as:

    [foo] => Array
        (
            [@attributes] => Array
                (
                    [somenum] => 333
                )
        )

## Conclusion

I'm not particularly proud of this workaround, but given the inability to affect the behavior of the proprietors of systems we request data from, you gotta do what you gotta do.

There's some good that came of this episode -- I'm learning a ton about XPath, XML Namespaces, the good, bad and the ugly of reading and writing SOAP encoding and a ton of other things.  I think I transcribed almost 100kb of XML by hand this week.  So, I'll mark this down as a learning experience.  Hopefully, I can write this code in a way that won't completely bewilder the next developer that has to touch it.

###### Update 2013-12-02:

I ended up not being able to use `kill_the_namespaces()` after all.  Unbeknownst to me, further down the execution chain there is a need to append nodes to the exact same structure to stage files for another system's ingestion.  If this was a read-only solution as I'd originally assumed, I'd be able to use the namespace remover and avoid having to put some even uglier code in this script, but alas no such luck for me (or the developer who is going to have to maintain this utility).

### Reference material:

1. [The "S" Stands for Simple](http://wanderingbarque.com/nonintersecting/2006/11/15/the-s-stands-for-simple/)
2. [DOMElement::removeAttributeNS()](http://www.php.net/manual/en/domelement.removeattributens.php)
3. [SimpleXML, Namespaces & Hair loss](http://blog.preinheimer.com/index.php?/archives/172-SimpleXML,-Namespaces-Hair-loss.html)
