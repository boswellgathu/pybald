#!/usr/bin/env python
# encoding: utf-8

from webob import Request, Response

class UserManager(object):
    '''Code to users, implemented as WSGI middleware.'''

    def __init__(self, application=None, user_class=None):
        self.user_class = user_class
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self,environ,start_response):
        req = Request(environ)

        session = environ.get('pybald.session', None)
        if session and session.user and session.user.can_login:
            environ['REMOTE_USER'] = session.user
        else:
            environ['REMOTE_USER'] = None

        # update or create the pybald.extension to populate controller
        # instances
        environ['pybald.extension'] = environ.get('pybald.extension', {})
        environ['pybald.extension']['user'] = environ['REMOTE_USER']

        # call the next part of the pipeline
        resp = req.get_response(self.application)
        return resp(environ,start_response)
