#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010. José Dinuncio
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License.
#
##############################################################################
import sys
from cStringIO import StringIO

from nose import with_setup
from pyforth import Forth


forth = None

# ==============================================================================
#    Support
# ==============================================================================
def init(fin=sys.stdin, fout=sys.stdout):
    '''init a forth machine'''
    global forth
    forth = Forth(run=False, fin=fin, fout=fout)

def assert_stack(stack):
    '''The forth stack must be equal to stack'''
    assert forth.stack == stack, 'result: %s || wait: %s' % (forth.stack, stack)

def check_code(code, ini_stack, end_stack):
    '''Executing code with ini_stack must end with end_stack'''
    forth.compile_word('init', code)
    forth.stack = ini_stack
    forth._run()
    assert_stack(end_stack)


# ==============================================================================
#    Tests
# ==============================================================================
@with_setup(init)
def test_load_dct():
    '''_load_dct'''
    for word in 'dup + /mod'.split():
        assert word in forth.dct, forth.dct

@with_setup(init)
def test_dup():
    '''dup'''
    check_code('dup end', [2], [2, 2])

@with_setup(init)
def test_lit():
    '''lit'''
    check_code('lit 3 end', [], [3])

@with_setup(init)
def test_branch():
    '''branch'''
    check_code('branch 1 drop end', [4], [4])

@with_setup(init)
def test_zbranch():
    '''0branch'''
    check_code('lit 1 + dup lit 3 = 0branch -9 end', [1], [3])

# I/O

def test_key():
    '''key'''
    fin = StringIO('abc')
    init(fin=fin)
    check_code('key key key end', [], ['a', 'b', 'c'])

def test_word():
    '''word'''
    fin = StringIO(' hello world ')
    init(fin=fin)
    check_code('word word end', [], ['hello', 'world'])

def test_emit():
    '''emit'''
    fout = StringIO()
    init(fout=fout)
    check_code('lit a emit end', [], [])
    assert fout.getvalue() == 'a', fout.getvalue()

# Dictionary words

@with_setup(init)
def test_store():
    '''store'''
    assert 'my' not in forth.dct, "'my' defined"
    check_code('lit 5 lit my ! end', [], [])
    assert 'my' in forth.dct, "'my' not defined"
    assert forth.dct['my'] == 5, forth.dct['my'] 

@with_setup(init)
def test_create():
    '''create, tick and comma'''
    assert 'blah' not in forth.dct
    check_code('create ` end , end', ['blah'], [])
    assert 'blah' in forth.dct

@with_setup(init)
def test_immediate():
    '''immediate'''
    check_code('create immediate end', ['foo'], [])
    word = forth.dct['foo']
    assert word.imm == True

@with_setup(init)
def test_exit():
    '''exit'''
    forth.compile_word('double', 'lit 2 * exit')
    check_code('lit 3 double lit 1 + end', [], [7])

