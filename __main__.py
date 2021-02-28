#!/usr/bin/env ipython
# coding: utf-8
#
# This source code is distributed under the terms of the Bad Code License.
# You are forbidden to distribute software containing this code to end users, because it is bad.
#
#
# The_eye_loop:
#    This is bad and you should feel bad about it
# Mr P:
#    Lucas qué hiciste
#    LUCAS QUE HICISTE PORFAVOR PARALOOOAAAAAAAA
#    You need to stop.
# Meggg:
#    Por que hiciste esto
# Luxter77
#    Por que hice esto
#

from miwstawke import main

import pytz
import dateutil as du
import datetime as dt
import sys

class safelist(list):
    def get(self, index):
        try:
            return(int(self.__getitem__(index)))
        except IndexError:
            return(0)

if __name__ == '__main__':

    if(len(sys.argv) < 3):
        main()
    else:
        a = safelist(sys.argv[1:])
        main(pytz.utc.localize(dt.datetime(
            year=a.get(0),
            month=a.get(1),
            day=a.get(2),
            hour=a.get(3),
            minute=a.get(4),
            second=a.get(5),
)))
