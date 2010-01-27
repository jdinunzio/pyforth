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

from cStringIO import StringIO

from nose import with_setup
from pyforth import Forth, add_word


forth = None

# ==============================================================================
#    Support
# ==============================================================================
def init(fin='', fout=''):
    '''init a forth machine'''
    global forth
    if fin or fout:
        forth = Forth(run=False, fin=fin, fout=fout)
    else:
        forth = Forth(run=False)

def def_init(word, stack=[]):
    '''Deinfe the init word'''
    add_word(forth, 'init', word)
    forth.pc = ['init', 0]
    forth.stack = stack
    forth._run()

def assert_stack(stack):
    '''The forth stack must be equal to stack'''
    assert forth.stack == stack, 'result: %s || wait: %s' % (forth.stack, stack)

def check_init(def_, ini_stack, end_stack, fin=None, fout=None):
    '''Initialize forth and check_def'''
    init(fin=fin, fout=fout)
    check_def(def_, ini_stack, end_stack)

def check_def(def_, ini_stack, end_stack):
    '''
    Define and execute the init word and check that the stack end as assumed
    '''
    def_init(def_, ini_stack)
    assert_stack(end_stack)


# ==============================================================================
#    Tests
# ==============================================================================

@with_setup(init)
def test_load_dct():
    '''_load_dct'''
    for word in 'dup + /mod'.split():
        assert word in forth.dct, forth.dct

def test_dup():
    '''dup'''
    check_init('dup end', [2], [2, 2])

def test_lit():
    '''lit'''
    check_init('lit 3 end', [], [3])

def test_branch():
    '''branch'''
    check_init('branch 1 drop end', [4], [4])

def test_zbranch():
    '''0branch'''
    check_init('lit 1 + dup lit 3 = 0branch -9 end', [1], [3])

def test_key():
    '''key'''
    fin = StringIO('abc')
    check_init('key key key end', [], ['a', 'b', 'c'], fin=fin)

def test_word():
    '''word'''
    fin = StringIO(' hello world ')
    check_init('word word end', [], ['hello', 'world'], fin=fin)

def test_emit():
    '''emit'''
    fout = StringIO()
    check_init('lit a emit end', [], [], fout=fout)
    assert fout.getvalue() == 'a', fout.getvalue()

def test_fetch_n_store():
    '''Test fetch and store'''
    assert 'my' not in forth.dct, "'my' defined"
    check_init('lit 5 lit my ! end', [], [])
    assert 'my' in forth.dct, "'my' not defined"
    check_def('lit my @ end', [], [5])

