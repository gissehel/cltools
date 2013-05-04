#!/usr/bin/env python

import sys
import os
from supertools import superable
from .i18n import _
from .exceptions import CLExitException
from .exceptions import CLInterruptException

@superable
class CLRunnable(object) :
    """A class to handle command line parsing/executing"""
    def __init__(self) :
        self._args = None
        self._tool_name = None
        
    def status(self, message) :
        sys.stdout.write((u'%s\n' % (message,)).encode('utf-8'))

    def error(self, message) :
        sys.stderr.write((_(u"Error : %s\n") % (message,)).encode('utf-8'))

    def errorexit(self, message) :
        self.error(message)
        raise CLExitException()

    def interruptexit(self) :
        raise CLInterruptException()

    def __print_general_parameters(self) :
        if len(self._cl_params['params'])>0 :
            print 'Global options:'
            names = sorted(set(self._cl_params['params'][param_name]['name'] for param_name in self._cl_params['params']))
            for name in names :
                param = self._cl_params['params'][name]
                namevalue = name
                if param['need_value'] :
                    namevalue = _('%s=VALUE') % (name,)
                print '    --%-18s %-40s' % (namevalue, param['doc'] or '')
                if len(param['aliases'])>1 :
                    print '%s (%s)' % (' '*24,','.join(sorted(['-','--'][int(len(alias)>1)]+alias for alias in param['aliases'])))
            print ''

    def help(self,args=[],kwargs={}) :
        tool_name = self._tool_name 
        if tool_name is None :
            tool_name = ''
        else :
            tool_name = tool_name + ' '

        print _("Usage: %s[GLOBAL OPTIONS] COMMAND_NAME [OPTIONS] [VALUES]") % (tool_name,)
        if self._cl_params['doc'] is not None :
            print self._cl_params['doc']
        print ''
        if len(self._cl_params['commands'])>0 :
            print 'Commands:'
            names = sorted(set(self._cl_params['commands'][command_name]['name'] for command_name in self._cl_params['commands']))
            for name in names :
                command = self._cl_params['commands'][name]
                print '    %-20s %-40s' % (name, command['doc'] or '')
                if len(command['aliases'])>1 :
                    print '%s (%s)' % (' '*24,','.join(sorted(command['aliases'])))
            print ''
        self.__print_general_parameters()

    def help_on_command(self, command, **kwargs) :
        """Get help on a specific command (typically for --help global param)"""
        print _("Command: %s [OPTIONS] [VALUES]") % (command['name'],)
        if command['doc'] is not None :
            print command['doc']
        print ''
        if len(command['params'])>0 :
            print 'Command options:'
            names = sorted(set(command['params'][param_name]['name'] for param_name in command['params']))
            for name in names :
                param = command['params'][name]
                namevalue = name
                if param['need_value'] :
                    namevalue = _('%s=VALUE') % (name,)
                print '    --%-18s %-40s' % (namevalue, param['doc'] or '')
                if len(param['aliases'])>1 :
                    print '%s (%s)' % (' '*24,','.join(sorted(['-','--'][int(len(alias)>1)]+alias for alias in param['aliases'])))
            print ''
        self.__print_general_parameters()
        self.interruptexit()

    def parse(self,args) :
        if len(args) == 0 :
            self.errorexit(_("Unexpected argument in parse method : first argument must be command line executable name"))
        self._tool_name = args[0]
        if self._tool_name in ('',None) :
            self._tool_name = None
        else :
            self._tool_name = os.path.basename(self._tool_name)

        command_name = None
        needed_arguments = []
        ordered_args = []
        command = None
        dict_args = {}
        parameter_hooks = []

        for arg in args[1:] :
            if arg.startswith('--') :
                if len(needed_arguments) > 0 :
                    (prev_arg_letter,prev_arg,prev_param) = needed_arguments[0]
                    self.errorexit(_("Switch [-%s] need parameter in [%s]") % (prev_arg_letter,prev_arg))
                arg_parts = arg.split('=',1)
                arg_name = arg_parts[0][2:]
                if command is None or arg_name not in command['params'] :
                    if arg_name not in self._cl_params['params'] :
                        self.errorexit(_("Don't know [%s] in param [%s]" % (arg_name, arg)))
                    else :
                        param = self._cl_params['params'][arg_name]
                else :
                    param = command['params'][arg_name]

                dict_args[param['name']] = arg_parts[1] if len(arg_parts) > 1 else param['default']
                if param['code'] is not None :
                    parameter_hooks.append((param['code'],param['name'],dict_args[param['name']]))

            elif arg.startswith('-') and len(arg)>1 :
                if len(needed_arguments) > 0 :
                    (prev_arg_letter,prev_arg,prev_param) = needed_arguments[0]
                    self.errorexit(_("Switch [-%s] need parameter in [%s]") % (prev_arg_letter,prev_arg))
                for arg_letter in arg[1:] :
                    if command is None or arg_letter not in command['params'] :
                        if arg_letter not in self._cl_params['params'] :
                            self.errorexit(_("Don't know [%s] in switch [%s]") % (arg_letter, arg))
                        else :
                            param = self._cl_params['params'][arg_letter]
                    else :
                        param = command['params'][arg_letter]

                    if param['need_value'] :
                        needed_arguments.append((arg_letter,arg,param))
                    else :
                        dict_args[param['name']] = param['default']
                        if param['code'] is not None :
                            parameter_hooks.append((param['code'],param['name'],dict_args[param['name']]))
            else :
                if len(needed_arguments) > 0 :
                    (prev_arg_letter,prev_arg,prev_param) = needed_arguments[0]
                    dict_args[prev_param['name']] = arg
                    if prev_param['code'] is not None :
                        parameter_hooks.append((prev_param['code'],prev_param['name'],dict_args[prev_param['name']]))

                    needed_arguments.pop(0)
                else :
                    if command is None :
                        command_name = arg
                        if command_name in self._cl_params['commands'] :
                            command = self._cl_params['commands'][command_name]
                        else :
                            self.help()
                            self.errorexit(_("No command named [%s]") % (command_name,))
                    else :
                        ordered_args.append(arg)
        if command_name is None :
            self.help()
            self.errorexit(_("Need a command name"))
        if len(needed_arguments) > 0 :
            (prev_arg_letter,prev_arg,prev_param) = needed_arguments[0]
            self.errorexit(_("Switch [-%s] need parameter in [%s]") % (prev_arg_letter,prev_arg))
        for code, name, value in parameter_hooks :
            code(self, args=ordered_args, kwargs=dict_args, name=name, value=value, command=command)
        command['code'](self,args=ordered_args,kwargs=dict_args)
            
    def run(self,args) :
        try :
            self.parse(args)
        except CLExitException :
            return False
        except CLInterruptException :
            return True
        return True

