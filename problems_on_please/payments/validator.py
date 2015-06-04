#!/usr/bin/env python3
# -*- coding: utf8 -*-

import testlib

limit = testlib.Limit.interval
ensure = testlib.Error.ensure
LIMIT_P = limit(0, 2 * 10**9)
LIMIT_TEST = 1000

def validate ( inf ):
    tc = 0
    while not inf.eof():
        name, p = inf.read("%s %d\n",[testlib.Limit.all(), LIMIT_P])
        if name == '' :
            break
        tc += 1
        ensure(tc <= LIMIT_TEST, 'too many tests')
    inf.close()

testlib.validator(validate)