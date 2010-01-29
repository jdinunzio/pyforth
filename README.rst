pyforth
=======

pyforth is an implementation of forth using the python language. I create to
better understand the forth interpreter. It is intended to be a clear, 
high-level implementation. pyforth was inspired by 
`jonesforth http://www.annexia.org/_file/jonesforth.s.txt`, an assembly 
implementation for linux machines.

Installation and Execution
==========================

You can download pyforth from github::

    $ git clone git@github.com:jdinuncio/pyforth.git

To install it, type::

    $ cd pyforth
    $ python setup.py install

But you can execute it without install it::

    $ pyforth/forthvm.py

Then you can start typing forth expressions::

    1 1 +
    : double 2 * ;
    bye

