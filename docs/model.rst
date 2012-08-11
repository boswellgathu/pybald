Models and ORM
==============

Pybald models are a fairly thin wrapper around the `SqlAlchemy <http://sqlalchemy.org/>`_ ORM.

.. automodule:: pybald.db.models

:class:`Model` - provide object data methods
-----------------------------------------------

.. autoclass:: Model
  :members: query, load, get, all, save, delete, flush, commit
  :undoc-members: