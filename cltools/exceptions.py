#!/usr/bin/env python

class CLException(Exception) : pass
class CLExitException(CLException) : pass
class CLInterruptException(CLException) : pass

