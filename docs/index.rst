pyramid_zcml
============

Overview
--------

``pyramid_zcml`` is a package which provides ZCML directives for all built-in Pyramid configuration directives.

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

At this point, it will be possible to use the
:func:`pyramid_zcml.load_zcml` function as a method of the configurator,
ala:

.. code-block:: python
   :linenos:

   config.load_zcml(....)

More Information
----------------

.. toctree::
   :maxdepth: 1

   api.rst
   glossary.rst
   zcml.rst


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
