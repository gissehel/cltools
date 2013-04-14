#!/usr/bin/env python

import sys
from calclib import Calc
from cltools import CLRunner
from supertools import superable

@CLRunner.runnable()
@superable
class CalcTool(object) :
    '''A simple command-line wrapper for calclib'''    
    def __init__(self) :
        self._calc = Calc()


    def get_two_params(self, args) :
        if len(args) != 2 :
            # errorexit provided by CLRunnable parent
            self.errorexit("Need two values VALUE1 and VALUE2 as arguments")
        try :
            value1 = int(args[0])
        except Exception :
            self.errorexit("Value [%s] should be a valid number" % (args[0],))
        try :
            value2 = int(args[1])
        except Exception :
            self.errorexit("Value [%s] should be a valid number" % (args[1],))
        return value1, value2

    @CLRunner.command()
    def add(self, args, kwargs) :
        '''Add two values VALUE1 and VALUE2 given as parameters'''
        value1, value2 = self.get_two_params(args)
        value = self._calc.add(value1, value2)
        self.status("Result : [%s]" % (value,))

    @CLRunner.command()
    def mult(self, args, kwargs) :
        '''Multiplie two values VALUE1 and VALUE2'''
        value1, value2 = self.get_two_params(args)
        value = self._calc.mult(value1, value2)
        self.status("Result : [%s]" % (value,))

    @CLRunner.command()
    def help(self, args=[], kwargs={}) :
        '''Get this help'''
        self.__super.help()

if __name__ == '__main__' :
    calctool = CalcTool()
    if not(calctool.run( sys.argv )) :
        sys.exit(1)




