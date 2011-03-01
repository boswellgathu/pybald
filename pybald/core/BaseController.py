#!/usr/bin/env python
# encoding: utf-8
"""
BaseController.py

Base Controller that all PyBald controllers inherit from.

Created by mikepk on 2009-06-29.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from pybald.core.TemplateEngine import engine

from webob import Request, Response
from webob import exc
import re

from pybald.db.models import session
from pybald.util import camel_to_underscore

from routes import redirect_to
import project


# action / method decorator
# This decorator takes in the action method and adds some syntactic sugar around it.
# Allows the actions to work with WebOb request / response objects, and handles default
# behaviors, such as displaying the view when nothing is returned, or plain text
# if a string is returned.
def action(func):
    def replacement(self, environ, start_response):
        req = Request(environ)

        # add any url variables as members of the controller
        # TODO: setup a way to avoid collisions with existing members (data overriding view, 
        # possible sec hole)
        if req.urlvars:
            for key in req.urlvars.keys():
                #Set the controller object to contain the url variables
                # parsed from the dispatcher / router
                setattr(self,key,req.urlvars[key])

        # this code defines the template id to match against
        # template path = controller name + '/' + action name (except in the case of)
        # index
        self.template_id = camel_to_underscore(re.search('(\w+)Controller',self.__module__).group(1)) #.lower()
        # 'index' is a special name. The index action maps to the controller name (no action view)
        if not re.search(r'index|__call__',func.__name__):
            self.template_id += '/'+str(func.__name__)
                
        # add the pybald extension dict to the controller
        # object
        extension = req.environ.get('pybald.extension',None)
        if extension:
            for key in extension.keys():
                setattr(self,key,extension[key])

        # Return either the controllers _pre code, whatever 
        # is returned from the controller
        # or the view. So pre has precedence over 
        # the return which has precedence over the view
        resp = self._pre(req) or func(self,req) or self._view()

        # if the response is currently just a string
        # wrap it in a response object
        if isinstance(resp, basestring):
            resp = Response(body=resp)

        # run the controllers post code
        self._post(req,resp)

        return resp(environ, start_response)
    # restore the original function name
    replacement.__name__ = func.__name__
    return replacement

import os.path
asset_tag_cache = {}
class Page(dict):
    def __init__(self, version=None):
        self['title'] = None
        self['metas'] = []
        self['headers'] = []
        self.version = project.media_version
        self['asset_tags'] = {}

    def compute_asset_tag(self, filename):
        asset_tag = asset_tag_cache.get(filename, None)
        if not asset_tag:
            asset_tag = str(int(round(os.path.getmtime(os.path.join(project.get_path(),"content",filename.lstrip("/"))) )) ) 
            asset_tag_cache[filename] = asset_tag
        return asset_tag

    def add_js(self, filename):
        filename += '?v=%s' % (self.compute_asset_tag(filename))
        self['headers'].append('''<script type="text/javascript" src="%s"></script>''' % (str(filename)) )

    def add_css(self, filename, media="screen"):
        filename += '?v=%s' % (self.compute_asset_tag(filename))
        self['headers'].append('''<link type="text/css" href="%s" media="%s" rel="stylesheet" />''' % (str(filename),str(media)) )



class BaseController():
    '''Base controller that includes the view and a default index method.'''

    def __init__(self):
        '''Initialize the base controller with a page object. Page dictionary controls title, headers, etc...'''
        self.page = Page() #{'title':None,'metas':[],'headers':[]}
        self.error = None
        self.user = None
        self.session = None

        if project.page_options:
            for key in project.page_options.keys():
                setattr(self, key, project.page_options[key]) 
                
    @action
    def index(self,req):
        '''default index action'''
        pass
        
    def _pre(self,req):
        '''Code to run before any action.'''
        pass

    def _post(self,req,resp):
        '''Code to run after any action.'''
        # Closes the db Session object. Required to avoid holding sessions
        # indefinitely and overruning the sqlalchemy pool
        pass

    def _redirect_to(self,url,*pargs,**kargs):
        '''Redirect the controller'''
        return redirect_to(url,*pargs,**kargs)

    def _not_found(self,text=None):
        raise exc.HTTPNotFound(text)

    def _status(self,code):
        raise exc.status_map[int(code)]


    def _view(self,user_dict=None):
        '''Method to invoke the template engine and display a view'''
        view = engine
        # user supplied dictionary, otherwise create a dictionary
        # from the controller
        if user_dict:
            user_dict['template_id'] = self.template_id
            return view(user_dict)
        # View has access to all the internal attributes
        # inside the view (for Mako at least) the dictionary is copied
        else:
            return view(self.__dict__)
        
class BaseControllerTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()