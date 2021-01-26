---
date:    2014-02-16
subject: Setting up PHPUnit and NetBeans 7.4
tags:
    - phpunit
    - netbeans
    - unit testing
    - test driven development
abstract: |
    The last time I attempted to configure NetBeans to use PHPUnit is
    what drove me to write [Tester.php](https://github.com/dbazile/Tester.php).
    Second time's the charm!  In this post, I document the steps I
    took to successfully install PHPUnit 3.7 and configure NetBeans
    7.3 and 7.4 to be able to run the tests and use the Skeleton
    Generator.
---

## Instructions

I will make the following assumptions about your machine:

* PHP is already installed at `C:\PHP`
* NetBeans is already installed
* You have a PHP project in NetBeans called *MyWebApplication* located at `C:\sites\www.MyWebApplication.com`



### 1. Create the directories to hold PHPUnit and unit tests

Create the directories `C:\PHP\phpunit` and `C:\sites\MyWebApplication\testing`.

*Note that since you're doing this install manually, these can be wherever you want.  But the instructions from here will assume you used the aforementioned names.*



### 2. Download the two files you need from the PHPUnit homepage

Get **phpunit.phar** from [https://phar.phpunit.de/phpunit.phar](https://phar.phpunit.de/phpunit.phar).

Get **phpunit-skelgen.phar** from [https://phar.phpunit.de/phpunit-skelgen.phar](https://phar.phpunit.de/phpunit-skelgen.phar).

Save both of these files in `C:\PHP\phpunit`.



### 3. Create the batch file wrappers for the `.phar` files

Next, you will create two batch files **phpunit.bat** and **phpunit-skelgen.bat** that you're going to call whenever you want to run PHPUnit.  These files are also what you will point NetBeans to.

Again, save both of these files in `C:\PHP\phpunit`.

##### The contents of **phpunit.bat**:

```dos
@echo off
set PHPBIN=C:\PHP\php.exe
"%PHPBIN%" -d safe_mode=Off "C:\PHP\PHPUnit\phpunit.phar" %*
```

##### The contents of **phpunit-skelgen.bat**:

```dos
@echo off
set PHPBIN=C:\PHP\php.exe
"%PHPBIN%" -d safe_mode=Off "C:\PHP\PHPUnit\phpunit-skelgen.phar" %*
```

##### Test these on the command line with the following commands:

```dos
\php\phpunit\phpunit.bat --version
PHPUnit 3.7 by Sebastian Bergmann

\php\phpunit\phpunit-skelgen.bat --version
PHPUnit Skeleton Generator 1.2.1 by Sebastian Bergmann.
```


### 4. Tell NetBeans where PHPUnit is installed

In NetBeans, click on **Tools** > **Options**.  On the *Options* dialog, click the **PHP** tab, then the **Unit Testing** tab.

##### Set the following options and click **OK**:

<table>
	<thead>
		<tr>
			<th width="32%">Option</th>
			<th>Value</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>PHPUnit Script</th>
			<td><code>C:\PHP\phpunit\phpunit.bat</code></td>
		</tr>
		<tr>
			<th>Skeleton Generator Script</th>
			<td><code>C:\PHP\phpunit\phpunit-skelgen.bat</code></td>
		</tr>
	</tbody>
</table>



### 5. Enable testing on *MyWebApplication* project

In NetBeans, right click on *MyWebApplication* in the Project Explorer and click **Properties**.

##### On the *Project Properties* dialog, under the *Sources* and *PHPUnit* sections, set the following options and click **OK**:

<table>
	<thead>
		<tr>
			<th width="32%">Option</th>
			<th width="43%">Value</th>
			<th>Description</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th colspan="3" class="group">Sources</th>
		</tr>
		<tr>
			<th>Test Folder</th>
			<td><code>C:\sites\www.MyWebApplication.com\testing</code></td>
			<td><em>This is where the unit tests will live</em></td>
		</tr>
		<tr>
			<th colspan="3" class="group">PHPUnit</th>
		</tr>
		<tr>
			<th>Use Bootstrap</th>
			<td><strong>Checked</strong></td>
			<td><em>Optional<a href="#bootstrap" title="Click to see an example of the bootstrap script">**</a></em></td>
		</tr>
		<tr>
			<th>Bootstrap</th>
			<td><code>C:\sites\www.MyWebApplication.com\testing\bootstrap.php</code></td>
			<td><em>Optional <a href="#bootstrap" title="Click to see an example of the bootstrap script">**</a></em></td>
		</tr>
		<tr>
			<th>Run All *Test Files Using PHPUnit</th>
			<td><strong>Checked</strong></td>
			<td></td>
		</tr>
	</tbody>
</table>

***At this point, you can build and run unit tests from NetBeans without using the Skeleton Generator if you know what you're doing.***

*Note that if you have other testing plugins installed, you may see a Testing node which contains a PHPUnit child node among others.  If this is the case, on the Testing node, check the checkbox next to PHPUnit under Testing Providers.*



### 6. Run the Skeleton Generator on one of your classes

In the *Project Explorer*, click on the file you want to generate a test for.  Click on **Tools** > **Create Test** from the menu and it should create your unit test.  I believe the hot-key for this command defaults to `Ctrl+Shift+U`.

*Note that I get a warning modal saying "Tests were not generated for the following files: [...]" when I use this on my office workstation (NetBeans 7.4) even though the script executes without error and actually creates the tests.  I don't get these warnings with my work laptop (NetBeans 7.3).  I haven't figured out how to resolve this, but since it actually creates the files, it's more a nuissance than a show stopper.*

*Also note that, although it will attempt to create a directory structure in the testing folder corresponding to the source file's original location, there is a chance that NetBeans will not actually be able to move the file into it.  In that event, the test will be in the testing root directory (i.e., `C:\sites\www.MyWebApplication.com\testing`).  This is likely related to the issue above.*



### The moment of truth

Once you have used the Skeleton Generator to create a test and added at least one test method to it, you should be able to run tests from NetBeans.

In the *Project Explorer*, right click on the file you just generated a test for and click **Test**.  If you want to see the red and green bar (which I always do), click on **Window** > **Output** > **Test Results** to open the *Test Results* pane.



## And that's all, folks!
Reach out to me [@dbazile](https://github.com/dbazile/bazile.org/issues/new?title=setting-up-phpunit-and-netbeans-7-4) if there are any errors.

_(Updated 2015-09-10): Thanks to @minxian\_li for pointing out the errors I had in my `phpunit.bat` and `phpunit-skelgen.bat` scripts._


### Addendum

#### <a id="bootstrap"></a>How to Create and Set the Bootstrap script (optional)

The bootstrap is good for constructing an execution environment similar to the operating conditions of the class being tested.  Here is a contrived example for our imaginary NetBeans project *MyWebApplication*:

```php
<?php
define('PATH_BASE', '/sites/www.MyWebApplication.com');

chdir(PATH_BASE);

spl_autoload_register(function($name) {

    // Autoload anything in the mywebapplication namespace
    if (0 === strpos("mywebapplication\\", $name)) {
        $name = strreplace("\\", '/', $name);
        require $name;
    }

}, true, true);
?>
```

This file would be stored at `C:\sites\www.MyWebApplication.com\testing\bootstrap.php`, although you can name it whatever you want.


#### References

* [PHPUnit Homepage](http://phpunit.de/)
* [PHPUnit Documentation](http://phpunit.de/manual/current/en/index.html)
* [Writing Tests for PHPUnit](http://phpunit.de/manual/current/en/writing-tests-for-phpunit.html)
