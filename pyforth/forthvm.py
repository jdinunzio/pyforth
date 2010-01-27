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

def code(name=''):
    def dec(fn, name=name):
        if not name:
            name = getattr(fn, '__name__')
        fn.name = name
        fn.code = True
        return fn
    return dec

class Forth:

    def __init__(self, run=True, fin=sys.stdin, fout=sys.stdout):
        self.stack = []
        self.rstack = []
        self.pc = ['init', 0]
        self.dct = {}
        self.fin = fin
        self.fout = fout

        self._load_dct()
        if run:
            self._run()

    # Micro-instructions

    def debug(self):
        print 'rs: ', self.rstack
        print 'pc: ', self.pc
        print 'wd: ', self.dct[self.pc[0]]
        print '    ', self.stack
        print

    def _run(self):
        '''Start running the virtual machine'''
        while True:
            self.debug()
            word = self._get_pc_word()
            if word == 'end':
                return
            self._exec(word)

    def _exec(self, word):
        '''Exec a word'''
        if self._is_code(word):
            self._exec_code(word)
        else:
            self._exec_def(word)

    def _exec_code(self, word):
        '''Exec a codeword'''
        wd = self.dct[word]
        wd()

    def _exec_def(self, word):
        '''Exec a defword'''
        self._rpush(self.pc)
        self.pc = [word, 0]

    def _is_code(self, word):
        '''Is the word a codeword?'''
        wd = self.dct[word]
        return getattr(wd, 'code', False)

    def _get_pc_word(self):
        '''Get the word referenced by the pc'''
        curword, idx = self.pc
        word = self._get_word(curword, idx)
        self._inc_pc()
        return word

    def _get_word(self, word, idx):
        '''Given a defword, returns its i-th word'''
        return self.dct[word][idx]

    def _inc_pc(self, i=1):
        '''Increment the program counter'''
        idx = self.pc[1]
        self.pc[1] = idx + i

    def _push(self, v):
        self.stack.append(v)

    def _pop(self):
        return self.stack.pop()

    def _rpush(self, v):
        self.rstack.append(v)

    def _rpop(self):
        return self.rstack.pop()

    def _load_dct(self):
        '''Load the dictionary with the codewords'''
        for name in dir(self):
            word = getattr(self, name)
            if getattr(word, 'code', False):
                name = getattr(word, 'name')
                self._add_word(name, word)

    def _add_word(self, name, word):
        self.dct[name] = word


    # Instructions

    # Stack instructions
    @code()
    def dup(self):
        v = self.stack[-1]
        self._push(v)

    @code()
    def drop(self):
        self._pop()

    @code()
    def swap(self):
        b = self._pop()
        a = self._pop()
        self._push(b)
        self._push(a)

    @code()
    def over(self):
        v = self.stack[-2]
        self._push(v)

    @code()
    def rot(self):
        c = self._pop()
        b = self._pop()
        a = self._pop()
        self._push(b)
        self._push(c)
        self._push(a)

    @code('rot-')
    def rot(self):
        c = self._pop()
        b = self._pop()
        a = self._pop()
        self._push(b)
        self._push(c)
        self._push(a)

    @code()
    def depth(self):
        d = len(self.stack)
        self._push(d)

    @code()
    def pick(self):
        i = self._pop()
        v = self.stack[-1 - i]
        self._push(v)

    # Arithmetic
    @code('+')
    def add(self):
        b = self._pop()
        a = self._pop()
        self._push(a+b)

    @code('-')
    def sub(self):
        b = self._pop()
        a = self._pop()
        self._push(a-b)

    @code('*')
    def mul(self):
        b = self._pop()
        a = self._pop()
        self._push(a*b)

    @code('/')
    def x(self):
        b = self._pop()
        a = self._pop()
        self._push(a/b)

    @code('/mod')
    def divmod(self):
        b = self._pop()
        a = self._pop()
        self._push(a/b)
        self._push(a%b)

    # Bit Operation
    @code('&')
    def b_and(self):
        b = self._pop()
        a = self._pop()
        self._push(a&b)

    @code('|')
    def b_or(self):
        b = self._pop()
        a = self._pop()
        self._push(a|b)

    @code('^')
    def b_xor(self):
        b = self._pop()
        a = self._pop()
        self._push(a^b)

    @code('~')
    def neg(self):
        a = self._pop()
        self._push(~a)


    @code('<<')
    def shl(self):
        b = self._pop()
        a = self._pop()
        self._push(a<<b)

    @code('>>')
    def shr(self):
        b = self._pop()
        a = self._pop()
        self._push(a>>b)

    # Logic
    def __bool(self, v):
        if v:
            return -1
        else:
            return 0

    @code('and')
    def and_(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a and b)
        self._push(v)

    @code('or')
    def or_(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a or b)
        self._push(v)

    @code('not')
    def not_(self):
        a = self._pop()
        v = self.__bool(not a)
        self._push(v)

    # Comparison 

    @code('<=')
    def le(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a <= b)
        self._push(v)

    @code('<')
    def lt(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a < b)
        self._push(v)

    @code('>=')
    def ge(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a >= b)
        self._push(v)

    @code('>')
    def gt(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a > b)
        self._push(v)

    @code('=')
    def eq(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a == b)
        self._push(v)

    @code('<>')
    def ne(self):
        b = self._pop()
        a = self._pop()
        v = self.__bool(a != b)
        self._push(v)

    # Branch

    @code()
    def branch(self):
        v = self._get_pc_word()
        self._inc_pc(v)

    @code('0branch')
    def zbranch(self):
        c = self._pop()
        v = self._get_pc_word()
        if not c:
            self._inc_pc(v)

    #
    @code()
    def lit(self):
        a = self._get_pc_word()
        self._push(a)

    @code('!')
    def store(self):
        k = self._pop()
        v = self._pop()
        self.dct[k] = v

    @code('@')
    def fetch(self):
        k = self._pop()
        v = self.dct[k]
        self._push(v)

    # return stack

    @code('>r')
    def tor(self):
        a = self._pop()
        self._rpush(a)

    @code('r>')
    def fromr(self):
        a = self._rpop()
        self._push(a)

    @code()
    def rdrop(self):
        self._rpop()

    # I/O

    @code()
    def key(self):
        '''Read a char from fin'''
        c = self.fin.read(1)
        #c = ord(c)
        self._push(c)

    @code()
    def word(self):
        '''Read a word from fin'''
        w = ''
        spaces = ' \t\n\f'

        while True:
            c = self.fin.read(1)
            if (not c) or (c not in spaces):
                break

        w = w + c
        while True:
            c = self.fin.read(1)
            if (not c) or (c in spaces):
                break
            w = w + c
        self._push(w)

    @code()
    def emit(self):
        '''Write a char to fout'''
        c = self._pop()
        if type(c) == int:
            c = chr(c)
        self.fout.write(c)
        if c == '\n':
            self.fout.flush()



def try_word(f, word, stack):
    f.stack = stack
    word = word.split()
    f._add_word('init', word)
    f.pc = ['init', 0]
    f._run()


if __name__ == '__main__':
    from cStringIO import StringIO
    fin = StringIO(' Hello word')
    f = Forth(run=False, fin=fin)
    try_word(f, 'word word  end', [])

