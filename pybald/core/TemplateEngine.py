#!/usr/bin/env python
# encoding: utf-8
"""
TemplateEngine.py

Created by mikepk on 2009-06-29.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import project

from mako.template import Template
from mako.lookup import TemplateLookup

class TemplateEngine:
    '''The basic template engine, looks up templates and renders them. Uses the mako template system'''
            
    def __init__(self): 
        self.project_path = project.get_path()
        self.default_template_path = os.path.join( os.path.dirname( os.path.realpath(__file__) ), 'default_templates' )
        fs_test = project.debug or False

        self.lookup = TemplateLookup(directories=[os.path.join(self.project_path,'app/views'), self.default_template_path], 
            module_directory=os.path.join(self.project_path,'viewscache'),
            imports=[
                'from pybald.core.helpers import link, img, humanize',
                ],
                input_encoding='utf-8',output_encoding='utf-8',
                filesystem_checks=fs_test)


    def form_render(self,template_name=None,**kargs):
        '''Render the form for a specific model using formalchemy.'''
        data = kargs
        try:
            data['template_id'] = kargs['fieldset'].template_id
        except (KeyError, AttributeError):
            data['template_id'] = 'forms/%s' % template_name
        return self.__call__(data,format="form")

        
    def __call__(self, data, format="html"):
        '''Callable method that executes the template.'''

        # if the data dictionary has a format, use that, 
        # otherwise default to the passed in value or html
        format = data.get("format", format) or "html"

        # TODO: Add memc caching of rendered templates
        mytemplate = self.lookup.get_template("/%s.%s.template" % (data['template_id'].lower(), format.lower()))
        return mytemplate.render(**data)

    def clear_viewscache(self):
        '''Clears out the viewscache. This isn't being used at the moment.'''
        folder = os.path.join(self.project_path,'viewscache')
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

engine = TemplateEngine()

class TemplateEngineTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()