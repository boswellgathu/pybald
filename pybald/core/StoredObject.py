#!/usr/bin/env python
# encoding: utf-8
"""
StoredObject.py

Created by mikepk on 2010-04-21.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import project

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

engine = sa.create_engine(project.get_engine(),**project.get_engine_args())
Session = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)

class StoredObject:
    '''Generic StoredObject all models inherit from.'''
    def __init__(self):
        self.session = None       

    def save(self,commit=False):
        if not self.session:
            self.session = Session()
        self.session.add(self)
        if commit:
            self.commit()
        return self

    def commit(self):
        '''Call the commit for the entire session (includes anything else pending)'''
        if not self.session:
            self.session = Session()
        self.session.commit()
        

    @classmethod
    def load(cls,**where):
        session = Session()
        return session.query(cls).filter_by(**where)

    class NotFound(Exception):
        pass

class StoredObjectTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()