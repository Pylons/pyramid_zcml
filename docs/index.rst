pyramid_zcml
============

Overview
--------

``pyramid_zcml`` is a package which provides :term:`ZCML` directives for all
built-in Pyramid configurator methods.

Installation
------------

Install using setuptools, e.g. (within a virtualenv)::

  $ easy_install pyramid_zcml

Setup
-----

Once ``pyramid_zcml`` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python
   :linenos:

   import pyramid_zcml

   config = Configurator(.....)
   config.include(pyramid_zcml)

Do this before trying to load any ZCML.  After this step is taken, it will be
possible to use the :func:`pyramid_zcml.load_zcml` function as a method of
the configurator, ala:

.. code-block:: python
   :linenos:

   config.load_zcml(....)

Paster Template
---------------

The ``pyramid_starter_zcml`` Paster template is included with this package.
You can use it via ``paster create -t pyramid_starter_zcml`` (on Pyramid 1.0,
1.1, or 1.2) or ``pcreate -s pyramid_starter_zcml`` (on Pyramid 1.3).  It
creates a package skeleton which configures a Pyramid appliction via ZCML.
The application performs URL mapping via :term:`traversal` and no persistence
mechanism.

Usage
-----

.. toctree::
   :maxdepth: 2

   narr.rst


Directives and API
------------------

.. toctree::
   :maxdepth: 2

   zcml.rst
   api.rst
   glossary.rst


Reporting Bugs / Development Versions
-------------------------------------

Visit http://github.com/Pylons/pyramid_zcml to download development or
tagged versions.

Visit http://github.com/Pylons/pyramid_zcml/issues to report bugs.

Indices and tables
------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
