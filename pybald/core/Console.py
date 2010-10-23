#!/usr/bin/env python
# encoding: utf-8
"""
Console.py

Created by mikepk on 2010-10-16.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""
import code
import sys

import readline
import atexit
import os

class Console(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.pybald-console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

