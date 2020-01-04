
# pyterpreter (WIP)
A tree-walk interpreter for a toy language, written in good ol' Python.

To fire up the REPL:

    $ python3  src/pyterpreter/preter.py
    >>> var a = 10;
    >>> print var;
    10.0
To execute a file, add an argument for the file's location:

    $ python3 src/pyterpreter/preter.py samples/print_somethings.pr

## Things that work right now
### Variables
Only two data types - numbers(all of which are floats) and strings

    >>> var a = 10;
    >>> var b = 0.5;
    >>> print a + b;
    10.5
    >>> var c = "Hello, Planet";
    >>> print c;
    Hello, Planet
    >>> var str = "talk to ";
    >>> var hand = "the hand!";
    >>> print str + hand;
    talk to the hand!
    >>> print str + "the hand!";
    talk to the hand!
### Control flow

    var first = 5;
    var second = 10;
    if(first > second){
	    print "oh no";
    }
    else{
	    print "perfect";
    }

### Loops

    var c = 10;
    while(c > 0){
	    print c;
    }
    
    for(var i=16; i>=1; i = i / 2){
	    print i;
    }
#
Based on [Crafting Interpreters](https://craftinginterpreters.com "Crafting Interpreters")
