#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

from webob import Request, Response

import logging
import logging.handlers
# import logging.Formatter

from textwrap import TextWrapper
class WrappedStream(object):
    def __init__(self, stream=sys.stderr):
        self.stream = stream
        self.sql_wrapper = TextWrapper(width=100,
                                       initial_indent=' '*15+'sql> ',
                                       subsequent_indent=' '*20)
    def write(self, text):
        wrapped_text = "{0}\n".format(self.sql_wrapper.fill(text))
        self.stream.write(wrapped_text)

    def flush(self, *pargs, **kargs):
        self.stream.flush(*pargs, **kargs)

engine_log = logging.getLogger('sqlalchemy.engine')

class WrappedFormatter(logging.Formatter):
    def __init__(self, *pargs, **kargs):
        logging.Formatter.__init__(self, *pargs, **kargs)
        self.sql_wrapper = TextWrapper(width=100,
                                       initial_indent=' ' * 15 + 'sql> ',
                                       subsequent_indent=' ' * 20)

    def format(self, record):
        # fmt = super(WrappedFormatter, self)
        fmt = logging.Formatter.format(self, record)
        wrapped_text = "{0}".format(self.sql_wrapper.fill(fmt))
        return wrapped_text

# custom stream handler that indents and formats SQL
h = logging.StreamHandler() #WrappedStream(sys.stderr))
formatter = WrappedFormatter("%(message)s")
h.setFormatter(formatter)
engine_log.addHandler(h)


def enable_sql_log():
    '''Function to turn on debug SQL output for SQLAlchemy'''
    # logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.ERROR)
    engine_log.setLevel(logging.INFO)


def disable_sql_log():
    '''Function to turn off debug SQL output for SQLAlchemy'''
    engine_log.setLevel(logging.ERROR)


class PybaldLogger(object):
    def __init__(self, application=None, log_file='/tmp/pybald.log',
                       level="DEBUG", project_name="Pybald"):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()
        LOG_FILENAME = log_file

        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger(project_name)
        log_level = getattr(logging, level)
        self.my_logger.setLevel(log_level)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME,
                      maxBytes=1024*1024*20,
                      backupCount=10)

        # create formatter
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s...%(message)s")
        # add formatter to handler
        handler.setFormatter(formatter)
        self.my_logger.addHandler(handler)
        self.write("Logger Started - %s" % level)


    def __call__(self,environ,start_response):
        req = Request(environ)
        sys.stdout = self
        sys.stderr = self
        #environ['wsgi.errors'] = self
        #pass through if no exceptions occur
        resp = req.get_response(self.application)
        return resp(environ,start_response)

    def write(self,msg):
        if msg == '\n':
            return
        self.my_logger.info(msg)


class PybaldLoggerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()