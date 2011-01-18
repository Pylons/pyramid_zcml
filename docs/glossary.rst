.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Pyramid
      A `web framework <http://pylonshq.com/pyramid>`_.

   View handler
     A view handler ties together
     :meth:`pyramid.config.Configurator.add_route` and
     :meth:`pyramid.config.Configurator.add_view` to make it more
     convenient to register a collection of views as a single class when
     using :term:`url dispatch`.  See also :ref:`views_chapter`.

   Pylons
     `A lightweight Python web framework <http://pylonshq.com>`_.

   URL dispatch
     An alternative to :term:`traversal` as a mechanism for locating a a
     :term:`view callable`.  When you use a :term:`route` in your Pyramid
     application via a :term:`route configuration`, you are using URL
     dispatch. See the :ref:`urldispatch_chapter` for more information.

   ZCML
     `Zope Configuration Markup Language
     <http://www.muthukadan.net/docs/zca.html#zcml>`_, an XML dialect
     used by Zope and Pyramid for configuration tasks.  ZCML
     is capable of performing different types of :term:`configuration
     declaration`, but its primary purpose in Pyramid is to
     perform :term:`view configuration` and :term:`route configuration`
     within the ``configure.zcml`` file in a Pyramid
     application.  You can use ZCML as an alternative to
     :term:`imperative configuration`.

   asset specification
     A colon-delimited identifier for an :term:`asset`.  The colon separates
     a Python :term:`package` name from a package subpath.  For example, the
     asset specification ``my.package:static/baz.css`` identifies the file
     named ``baz.css`` in the ``static`` subdirectory of the ``my.package``
     Python :term:`package`.  See :ref:`asset_specifications` for more info.

   view callable
     A "view callable" is a callable Python object which is associated with a
     :term:`view configuration`; it returns a :term:`response` object .  A
     view callable accepts a single argument: ``request``, which will be an
     instance of a :term:`request` object.  A view callable is the primary
     mechanism by which a developer writes user interface code within
     Pyramid.  See :ref:`views_chapter` for more information about Pyramid
     view callables.

   view
     Common vernacular for a :term:`view callable`.

   view predicate
     An argument to a :term:`view configuration` which evaluates to
     ``True`` or ``False`` for a given :term:`request`.  All predicates
     attached to a view configuration must evaluate to true for the
     associated view to be considered as a possible callable for a
     given request.

   traversal
     The act of descending "up" a tree of resource objects from a root
     resource in order to find a context resource.  The Pyramid
     :term:`router` performs traversal of resource objects when a :term:`root
     factory` is specified.  See the :ref:`traversal_chapter` chapter for
     more information.  Traversal can be performed *instead* of :term:`URL
     dispatch` or can be combined *with* URL dispatch.  See
     :ref:`hybrid_chapter` for more information about combining traversal and
     URL dispatch (advanced).

   imperative configuration
     The configuration mode in which you use Python to call methods on
     a :term:`Configurator` in order to add each :term:`configuration
     declaration` required by your application.

   route configuration
     Route configuration is the act of using :term:`imperative
     configuration` or a :term:`ZCML` ``<route>`` statement to
     associate request parameters with a particular :term:`route` using
     pattern matching and :term:`route predicate` statements.  See
     :ref:`urldispatch_chapter` for more information about route
     configuration.

   view configuration
     View configuration is the act of associating a :term:`view callable`
     with configuration information.  This configuration information helps
     map a given :term:`request` to a particular view callable and it can
     influence the response of a view callable.  Pyramid views can be
     configured via :term:`imperative configuration`, :term:`ZCML` or by a
     special ``@view_config`` decorator coupled with a :term:`scan`.  See
     :ref:`view_config_chapter` for more information about view
     configuration.

   configuration declaration
     An individual method call made to an instance of a Pyramid
     :term:`Configurator` object which performs an arbitrary action, such as
     registering a :term:`view configuration` (via the ``add_view`` method of
     the configurator) or :term:`route configuration` (via the ``add_route``
     method of the configurator).

   request
     A ``WebOb`` request object.  See :ref:`webob_chapter` (narrative)
     and :ref:`request_module` (API documentation) for information
     about request objects.

   scan
     The term used by Pyramid to define the process of
     importing and examining all code in a Python package or module for
     :term:`configuration decoration`.

   route
     A single pattern matched by the :term:`url dispatch` subsystem, which
     generally resolves to one or more :term:`view callable` objects.  See
     also :term:`url dispatch`.

   asset
     Any file contained within a Python :term:`package` which is *not*
     a Python source code file.

   asset specification
     A colon-delimited identifier for an :term:`asset`.  The colon separates
     a Python :term:`package` name from a package subpath.  For example, the
     asset specification ``my.package:static/baz.css`` identifies the file
     named ``baz.css`` in the ``static`` subdirectory of the ``my.package``
     Python :term:`package`.  See :ref:`asset_specifications` for more info.

   package
     A directory on disk which contains an ``__init__.py`` file, making
     it recognizable to Python as a location which can be ``import`` -ed.
     A package exists to contain :term:`module` files.

   module
     A Python source file; a file on the filesystem that typically ends with
     the extension ``.py`` or ``.pyc``.  Modules often live in a 
     :term:`package`.

   configurator
     An object used to do :term:`configuration declaration` within an
     application.  The most common configurator is an instance of the
     ``pyramid.config.Configurator`` class.

   route predicate
     An argument to a :term:`route configuration` which implies a value
     that evaluates to ``True`` or ``False`` for a given
     :term:`request`.  All predicates attached to a :term:`route
     configuration` must evaluate to ``True`` for the associated route
     to "match" the current request.  If a route does not match the
     current request, the next route (in definition order) is
     attempted.

   root factory
     The "root factory" of an Pyramid application is called
     on every request sent to the application.  The root factory
     returns the traversal root of an application.  It is
     conventionally named ``get_root``.  An application may supply a
     root factory to Pyramid during the construction of a
     :term:`Configurator`.  If a root factory is not supplied, the
     application uses a default root object.  Use of the default root
     object is useful in application which use :term:`URL dispatch` for
     all URL-to-view code mappings.

   configuration decoration
     Metadata implying one or more :term:`configuration declaration`
     invocations.  Often set by configuration Python :term:`decorator`
     attributes, such as :class:`pyramid.view.view_config`, aka
     ``@view_config``.

   decorator
     A wrapper around a Python function or class which accepts the function
     or class as its first argument and which returns an arbitrary object.
     Pyramid provides several decorators, used for configuration and return
     value modification purposes.  See also `PEP 318
     <http://www.python.org/dev/peps/pep-0318/>`_.

   router
     The :term:`WSGI` application created when you start a
     Pyramid application.  The router intercepts requests,
     invokes traversal and/or URL dispatch, calls view functions, and
     returns responses to the WSGI server on behalf of your
     Pyramid application.

   WSGI
     `Web Server Gateway Interface <http://wsgi.org/>`_.  This is a
     Python standard for connecting web applications to web servers,
     similar to the concept of Java Servlets.  Pyramid requires
     that your application be served as a WSGI application.

   dotted Python name
     A reference to a Python object by name using a string, in the form
     ``path.to.modulename:attributename``.  Often used in Paste and
     setuptools configurations.  A variant is used in dotted names
     within :term:`ZCML` attributes that name objects (such as the ZCML
     "view" directive's "view" attribute): the colon (``:``) is not
     used; in its place is a dot.

   application registry
     A registry of configuration information consulted by
     Pyramid while servicing an application.  An application
     registry maps resource types to views, as well as housing other
     application-specific component registrations.  Every
     Pyramid application has one (and only one) application
     registry.

   view name
     The "URL name" of a view, e.g ``index.html``.  If a view is
     configured without a name, its name is considered to be the empty
     string (which implies the :term:`default view`).

   Default view
     The default view of a :term:`resource` is the view invoked when the
     :term:`view name` is the empty string (``''``).  This is the case when
     :term:`traversal` exhausts the path elements in the PATH_INFO of a
     request before it returns a :term:`context` resource.

   Zope Component Architecture
     The `Zope Component Architecture
     <http://www.muthukadan.net/docs/zca.html>`_ (aka ZCA) is a system
     which allows for application pluggability and complex dispatching
     based on objects which implement an :term:`interface`.
     Pyramid uses the ZCA "under the hood" to perform view
     dispatching and other application configuration tasks.

   Translation Directory
     A translation directory is a :term:`gettext` translation
     directory.  It contains language folders, which themselves
     contain ``LC_MESSAGES`` folders, which contain ``.mo`` files.
     Each ``.mo`` file represents a set of translations for a language
     in a :term:`translation domain`.  The name of the ``.mo`` file
     (minus the .mo extension) is the translation domain name.

   Translation Domain
     A string representing the "context" in which a translation was
     made.  For example the word "java" might be translated
     differently if the translation domain is "programming-languages"
     than would be if the translation domain was "coffee".  A
     translation domain is represnted by a collection of ``.mo`` files
     within one or more :term:`translation directory` directories.

   view mapper
    A view mapper is a class which implements the
    :class:`pyramid.interfaces.IViewMapperFactory` interface, which performs
    view argument and return value mapping.  This is a plug point for
    extension builders, not normally used by "civilians".

   authorization policy
     An authorization policy in Pyramid terms is a bit of
     code which has an API which determines whether or not the
     principals associated with the request can perform an action
     associated with a permission, based on the information found on the
     :term:`context` resource.

   Locale Negotiator
     An object supplying a policy determining which :term:`locale
     name` best represents a given :term:`request`.  It is used by the
     :func:`pyramid.i18n.get_locale_name`, and
     :func:`pyramid.i18n.negotiate_locale_name` functions, and
     indirectly by :func:`pyramid.i18n.get_localizer`.  The
     :func:`pyramid.i18n.default_locale_negotiator` function
     is an example of a locale negotiator.

   Locale Name
     A string like ``en``, ``en_US``, ``de``, or ``de_AT`` which
     uniquely identifies a particular locale.

   Default Locale Name
     The :term:`locale name` used by an application when no explicit
     locale name is set.  See :ref:`localization_deployment_settings`.

   Forbidden view
      An :term:`exception view` invoked by Pyramid when the
      developer explicitly raises a
      ``pyramid.exceptions.Forbidden`` exception from within
      :term:`view` code or :term:`root factory` code, or when the
      :term:`view configuration` and :term:`authorization policy`
      found for a request disallows a particular view invocation.
      Pyramid provides a default implementation of a
      forbidden view; it can be overridden.  See
      :ref:`changing_the_forbidden_view`.

   Exception view
      An exception view is a :term:`view callable` which may be
      invoked by Pyramid when an exception is raised during
      request processing.  See :ref:`exception_views` for more
      information.

   Not Found view
      An :term:`exception view` invoked by Pyramid when the
      developer explicitly raises a ``pyramid.exceptions.NotFound``
      exception from within :term:`view` code or :term:`root factory`
      code, or when the current request doesn't match any :term:`view
      configuration`.  Pyramid provides a default
      implementation of a not found view; it can be overridden.  See
      :ref:`changing_the_notfound_view`.

   default permission
     A :term:`permission` which is registered as the default for an
     entire application.  When a default permission is in effect,
     every :term:`view configuration` registered with the system will
     be effectively amended with a ``permission`` argument that will
     require that the executing user possess the default permission in
     order to successfully execute the associated :term:`view
     callable` See also :ref:`setting_a_default_permission`.

   renderer
     A serializer that can be referred to via :term:`view
     configuration` which converts a non-:term:`Response` return
     values from a :term:`view` into a string (and ultimately a
     response).  Using a renderer can make writing views that require
     templating or other serialization less tedious.  See
     :ref:`views_which_use_a_renderer` for more information.

   renderer factory
     A factory which creates a :term:`renderer`.  See
     :ref:`adding_and_overriding_renderers` for more information.

   authentication policy
     An authentication policy in Pyramid terms is a bit of
     code which has an API which determines the current
     :term:`principal` (or principals) associated with a request.

   ZCML declaration
     The concrete use of a :term:`ZCML directive` within a ZCML file.

   ZCML directive
     A ZCML "tag" such as ``<view>`` or ``<route>``.

   Resource Location
     The act of locating a :term:`context` resource given a :term:`request`.
     :term:`Traversal` and :term:`URL dispatch` are the resource location
     subsystems used by Pyramid.

