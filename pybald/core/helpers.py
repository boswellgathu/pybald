#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

A set of HTML helpers for the templates. This includes link generating code, and special
escaping code.

Created by mikepk on 2009-07-08.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

#url_for takes these arguments as well
# anchor          specified the anchor name to be appened to the path
# host            overrides the default (current) host if provided
# protocol        overrides the default (current) protocol if provided
# qualified       creates the URL with the host/port information as 
#                 needed

# TODO: add javascript escape code here so it's available in the template engine

from routes import url_for


def url_route(*pargs,**kargs):
    '''Why doesn t url_for work?'''
    return url_for(*pargs,**kargs)

def link_to(text=None, route=None, alt=None, **args):
    '''A small function to help generate links in templates.'''
    if route:
        url = url_for(route,**args)
    else:
        url = url_for(**args)

    if not text:
        text = url
        
    if not alt:
        alt = text
        
    return '''<a href="%s" >%s</a>''' % (url,text)


def link_img_to(src=None, route=None, alt=None, style_id=None, **args):
    '''A small function to help generate img links in templates.'''
    if not src:
        return ''
    
    id_text = ''
    if style_id:
        id_text = '''id="%s" ''' % (style_id)
    
    if route:
        url = url_for(route,**args)
    else:
        url = url_for(**args)
    
    if not alt:
        alt = src
    
    return '''<a href="%s" ><img %ssrc="%s" alt="%s" /></a>''' % (url,id_text,src,alt)
