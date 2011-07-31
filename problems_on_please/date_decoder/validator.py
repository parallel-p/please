#!/usr/bin/env python3
# -*- coding: utf8 -*-

import testlib

day_limit = 32
year_limit = 100

limit = testlib.Limit.interval
ensure = testlib.Error.ensure

def validate ( inf ):
    tmpstr = inf.read("%s",[testlib.Limit.all()])[0]
    ansstr = tmpstr.split('-')

    ensure(int(ansstr[0]) < day_limit, "big day!")
    ensure(int(ansstr[2]) < year_limit, "big year!")
    ensure(len(ansstr[1]) == 3, "not a month")

    inf.close()

testlib.validator(validate)