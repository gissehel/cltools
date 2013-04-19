#!/usr/bin/env python

import time
# import yaml

from .runnable import CLRunnable

class CLRunner(object) :
    """A class that provide decorators to transform a class into a command line tool"""
    @staticmethod
    def _normalize_param(param,name=None) :
            if param is None :
                param = {}
            new_param = {}
            new_param['name'] = name
            new_param['need_value'] = param['need_value'] if ('need_value' in param) else False
            new_param['default'] = param['default'] if ('default' in param) else None
            new_param['aliases'] = [name] + (param['aliases'] if 'aliases' in param else [])
            new_param['doc'] = param['doc'] if ('doc' in param) else None
            new_param['code'] = param['code'] if ('code' in param) else None
            return new_param

    @staticmethod
    def _normalize_params(params) :
        new_params = {}
        for name in params :
            param = params[name]
            new_param = CLRunner._normalize_param(param,name)
            for alias in new_param['aliases'] :
                new_params[alias] = new_param
        return new_params

    @staticmethod
    def param(**kwargs) :
        def result(method) :
            param = CLRunner._normalize_param( kwargs, kwargs['name'] if 'name' in kwargs else method.func_name )
            if param['doc'] is None :
                param['doc'] = method.func_doc
            method._cl_param = param
            return method
        return result

    @staticmethod
    def command(name=None,params=None,aliases=None,doc=None) :
        def result(method) :
            command_name = method.func_name if name is None else name
            command_doc = method.func_doc if doc is None else doc
            method._cl_command = {
                'name' : command_name,
                'params' : CLRunner._normalize_params( {} if params is None else params ),
                'aliases' : [command_name] if aliases is None else [command_name] + aliases,
                'doc' : command_doc,
                }
            return method
        return result

    @staticmethod
    def runnable(name=None,params={},runnable=None,runnable_args=None,runnable_kwargs=None,doc=None) :
        if runnable is None :
            runnable = CLRunnable
        if runnable_args is None :
            runnable_args = []
        if runnable_kwargs is None :
            runnable_kwargs = {}
        def result(cls) :
            class command_line_runnable(cls, runnable) :
                def __init__(self, *args, **kwargs) :
                    cls.__init__(self, *args, **kwargs)
                    runnable.__init__(self,*runnable_args,**runnable_kwargs)
            runnable_name = cls.__name__ if name is None else name
            commands = {}
            global_params = CLRunner._normalize_params(params)

            for attrname in dir(command_line_runnable) :
                item = getattr(command_line_runnable,attrname)
                if hasattr(item,'_cl_command') :
                    command = {
                        'name' : item._cl_command['name'],
                        'params' : item._cl_command['params'],
                        'aliases' : item._cl_command['aliases'],
                        'doc' : item._cl_command['doc'] if item._cl_command['doc'] is not None else item.func_doc,
                        'code' : item,
                        }
                    delattr(item.im_func,'_cl_command')
                    for alias in command['aliases'] :
                        commands[alias] = command
                if hasattr(item,'_cl_param') :
                    param = item._cl_param
                    param['code'] = item
                    delattr(item.im_func,'_cl_param')
                    for alias in param['aliases'] :
                        global_params[alias] = param

            command_line_runnable.__name__ = cls.__name__

            command_line_runnable._cl_params = {
                'name' : runnable_name,
                'params' : global_params,
                'commands' : commands,
                'doc' :  cls.__doc__ if doc is None else doc,
                }
            # print yaml.dump(command_line_runnable._cl_params,default_flow_style=False)
            return command_line_runnable
        return result

