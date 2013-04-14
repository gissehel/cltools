cltools
=======

Set of decorators of  to create transform a class into a command-line tool

Imagine, you've got a class you want to use from the command line, without having
to explicitly parse the command line and make all the routing stuff.

That's what's ``cltools`` is doing by proving decorators on class and methods to make your
class runnable, and transform your method into commands.

``cltools`` create command tools like git/hg/svn/apt-get/apt-cache/..., that means your
tool will have commands

simple example :
----------------

Imagine, you've got a simple class that make tasks, and you want to make a command line tool
with that. Let's say, it's a calculator module ``calclib.py`` :

::
    
    #:/usr/bin/env python
    
    class Calc(object) :
        def __init__(self) :
            pass
        def add(self, value1, value2) :
            return value1+value2
        def mult(self, value1, value2) :
            return value1*value2

Then, we will write a simple class and transform into a runnable tool :

::
    
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

Now we can test our command line tool :

::
    
    $ ./calc.py
    Usage: calc.py COMMAND_NAME [OPTION] [VALUES]
    A simple command-line wrapper for calclib

    Commands:
        add                  Add two values VALUE1 and VALUE2 given as parameters
        help                 Get this help
        mult                 Multiplie two values VALUE1 and VALUE2
    
    Error : Need a command name

::
    
    $ ./calc.py add 4 17
    Result : [21]

::
    
    $ ./calc.py add 15 66 33
    Error : Need two values VALUE1 and VALUE2 as arguments

Note that the help is aumatically generate based on commands declared in the class, 
and the online doc attached to the class and methods.




