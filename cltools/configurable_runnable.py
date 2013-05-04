#!/usr/bin/env python

import os
import json

from supertools import superable
# from .i18n import _
from .runnable import CLRunnable

@superable
class ConfigurableCLRunnable(CLRunnable) :
    """A subclass of CLRunnable that provide configuration file reading/writing"""
    def __init__(self, config_dirname, config_filename, profile=None) :
        self.__super.__init__()
        self._configuration_dirname = os.path.expanduser(config_dirname)
        self._configuration_filename = config_filename
        self.__profile = profile
        self.load_config()

    def export_config(self) :
        return {}

    def import_config(self,config) :
        pass

    def get_profile(self) :
        return self.__profile

    def set_profile(self, profile) :
        self.__profile = profile

    def get_configuration_dirname(self) :
        if self._profile is None :
            return self._configuration_dirname
        return os.path.join(self._configuration_dirname, '__profiles__', self.__profile)

    def save_stream(self, name, stream) :
        dirname = self.get_configuration_dirname()
        if not(os.path.exists(dirname)) :
            os.makedirs(dirname,mode=0700);
        filename = os.path.join(dirname, name)
        with open(filename,'wb') as handle :
            json.dump(stream,handle,indent=2)

    def load_stream(self,name) :
        filename = os.path.join(self.get_configuration_dirname(), name)
        if os.path.exists(filename) :
            with open(filename,'rb') as handle :
                stream = json.load(handle)
            return stream
        return None

    def del_stream(self,name) :
        filename = os.path.join(self.get_configuration_dirname(), name)
        if os.path.exists(filename) :
            os.unlink(filename)

    def save_config(self) :
        self.save_stream(self._configuration_filename, self.export_config())

    def load_config(self) :
        config = self.load_stream(self._configuration_filename)
        if config != None :
            self.import_config(config)

    def run(self, args) :
        try :
            return self.__super.run(args)
        finally :
            self.save_config()

