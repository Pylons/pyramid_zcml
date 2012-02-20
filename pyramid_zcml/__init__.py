import os
import sys
import threading

from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Tokens
from zope.configuration.xmlconfig import registerCommonDirectives
from zope.configuration.config import ConfigurationMachine

from zope.interface import Interface
from zope.interface import implementedBy
from zope.interface import providedBy

from zope.schema import ASCIILine
from zope.schema import Bool
from zope.schema import Int
from zope.schema import TextLine

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid.authentication import RepozeWho1AuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.asset import asset_spec_from_abspath
from pyramid.threadlocal import get_current_registry

from zope.configuration import xmlconfig

###################### directives ##########################

class IViewDirective(Interface):
    context = GlobalObject(
        title=u"The interface or class this view is for.",
        required=False
        )

    for_ = GlobalObject(
        title=(u"The interface or class this view is for (alternate spelling "
               "of ``context``)."),
        required=False
        )

    permission = TextLine(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=False
        )

    view = GlobalObject(
        title=u"",
        description=u"The view function",
        required=False,
        )

    name = TextLine(
        title=u"The name of the view",
        description=u"""
        The name shows up in URLs/paths. For example 'foo' or 'foo.html'.""",
        required=False,
        )

    attr = TextLine(
        title=u'The callable attribute of the view object(default is __call__)',
        description=u'',
        required=False)

    renderer = TextLine(
        title=u'The renderer asssociated with the view',
        description=u'',
        required=False)

    wrapper = TextLine(
        title = u'The *name* of the view that acts as a wrapper for this view.',
        description = u'',
        required=False)

    request_type = GlobalObject(
        title=u"The dotted name interface for the request type",
        description=(u"The view will be called if the interface represented by "
                     u"'request_type' is implemented by the request.  The "
                     u"default request type is pyramid.interfaces.IRequest"),
        required=False
        )

    route_name = TextLine(
        title = u'The route that must match for this view to be used',
        required = False)

    containment = GlobalObject(
        title = u'Dotted name of a containment class or interface',
        required=False)

    request_method = TextLine(
        title = u'Request method name that must be matched (e.g. GET/POST)',
        description = (u'The view will be called if and only if the request '
                       'method (``request.method``) matches this string.'),
        required=False)

    request_param = TextLine(
        title = (u'Request parameter name that must exist in '
                 '``request.params`` for this view to match'),
        description = (u'The view will be called if and only if the request '
                       'parameter exists which matches this string.'),
        required=False)

    xhr = Bool(
        title = (u'True if request has an X-Requested-With header with the '
                 'value "XMLHttpRequest"'),
        description=(u'Useful for detecting AJAX requests issued from '
                     'jQuery, Protoype and other JavaScript libraries'),
        required=False)

    accept = TextLine(
        title = (u'Mimetype(s) that must be present in "Accept" HTTP header '
                 'for the view to match a request'),
        description=(u'Accepts a mimetype match token in the form '
                     '"text/plain", a wildcard mimetype match token in the '
                     'form "text/*" or a match-all wildcard mimetype match '
                     'token in the form "*/*".'),
        required = False)

    header = TextLine(
        title=u'Header name/value pair in the form "name=<regex>"',
        description=u'Regular expression matching for header values',
        required = False)

    path_info = TextLine(
        title = (u'Regular expression which must match the ``PATH_INFO`` '
                 'header for the view to match a request'),
        description=(u'Accepts a regular expression.'),
        required = False)

    decorator = GlobalObject(
        title = u'View decorator',
        required = False)

    mapper = GlobalObject(
        title = u'View mapper',
        required = False)

    custom_predicates = Tokens(
        title=u"One or more custom dotted names to custom predicate callables",
        description=(u"A list of dotted name references to callables that "
                     "will be used as predicates for this view configuration"),
        required=False,
        value_type=GlobalObject()
        )


def view(
    _context,
    permission=None,
    for_=None,
    view=None,
    name="",
    request_type=None,
    route_name=None,
    request_method=None,
    request_param=None,
    containment=None,
    attr=None,
    renderer=None,
    wrapper=None,
    xhr=False,
    accept=None,
    header=None,
    path_info=None,
    traverse=None,
    decorator=None,
    mapper=None,
    custom_predicates=(),
    context=None,
    cacheable=True, # not used, here for b/w compat < 0.8
    ):

    context = context or for_
    config = with_context(_context)
    config.add_view(
        permission=permission, context=context, view=view, name=name,
        request_type=request_type, route_name=route_name,
        request_method=request_method, request_param=request_param,
        containment=containment, attr=attr, renderer=renderer,
        wrapper=wrapper, xhr=xhr, accept=accept, header=header,
        path_info=path_info, custom_predicates=custom_predicates,
        decorator=decorator, mapper=mapper)

_view = view # for directives that take a view arg

class IRouteLikeDirective(Interface):
    """ The interface for the ``route`` ZCML directive
    """
    pattern = TextLine(title=u'pattern', required=False)
    factory = GlobalObject(title=u'context factory', required=False)
    view = GlobalObject(title=u'view', required=False)

    view_context = GlobalObject(title=u'view_context', required=False)
    # aliases for view_context
    for_ = GlobalObject(title=u'for', required=False)
    view_for = GlobalObject(title=u'view_for', required=False)

    view_permission = TextLine(title=u'view_permission', required=False)
    # alias for view_permission
    permission = TextLine(title=u'permission', required=False)

    view_renderer = TextLine(title=u'view_renderer', required=False)
    # alias for view_renderer
    renderer = TextLine(title=u'renderer', required=False)

    view_attr = TextLine(title=u'view_attr', required=False)

    request_method = TextLine(title=u'request_method', required=False)
    request_param = TextLine(title=u'request_param', required=False)
    header = TextLine(title=u'header', required=False)
    accept = TextLine(title=u'accept', required=False)
    xhr = Bool(title=u'xhr', required=False)
    path_info = TextLine(title=u'path_info', required=False)

    traverse = TextLine(
        title=u'Traverse pattern"',
        description=u'A pattern which will compose a traversal path',
        required = False)

    custom_predicates = Tokens(
        title=u"One or more custom dotted names to custom predicate callables",
        description=(u"A list of dotted name references to callables that "
                     "will be used as predicates for this view configuration"),
        required=False,
        value_type=GlobalObject()
        )
    use_global_views = Bool(title=u'use_global_views', required=False)

class IRouteDirective(IRouteLikeDirective):
    name = TextLine(title=u'name', required=True)
    # alias for pattern
    path = TextLine(title=u'path', required=False)

def route(_context,
          name,
          pattern=None,
          view=None,
          view_for=None,
          permission=None,
          factory=None,
          for_=None,
          header=None,
          xhr=False,
          accept=None,
          path_info=None,
          request_method=None,
          request_param=None,
          custom_predicates=(),
          view_permission=None,
          view_attr=None,
          renderer=None,
          view_renderer=None,
          view_context=None,
          traverse=None,
          use_global_views=False,
          path=None):
    """ Handle ``route`` ZCML directives
    """
    # the strange ordering of the request kw args above is for b/w
    # compatibility purposes.

    # these are route predicates; if they do not match, the next route
    # in the routelist will be tried
    if view_context is None:
        view_context = view_for or for_

    view_permission = view_permission or permission
    view_renderer = view_renderer or renderer

    if pattern is None:
        pattern = path

    if pattern is None:
        raise ConfigurationError('route directive must include a "pattern"')

    config = with_context(_context)
    if view:
        config.add_view(
            route_name=name,
            view=view,
            permission=view_permission,
            context=view_context,
            renderer=view_renderer,
            attr=view_attr)
    config.add_route(
        name,
        pattern,
        factory=factory,
        header=header,
        xhr=xhr,
        accept=accept,
        path_info=path_info,
        request_method=request_method,
        request_param=request_param,
        custom_predicates=custom_predicates,
        use_global_views=use_global_views,
        traverse=traverse,
        )

class ISystemViewDirective(Interface):
    view = GlobalObject(
        title=u"",
        description=u"The view function",
        required=False,
        )

    attr = TextLine(
        title=u'The callable attribute of the view object(default is __call__)',
        description=u'',
        required=False)

    renderer = TextLine(
        title=u'The renderer asssociated with the view',
        description=u'',
        required=False)

    wrapper = TextLine(
        title = u'The *name* of the view that acts as a wrapper for this view.',
        description = u'',
        required=False)

def notfound(_context,
             view=None,
             attr=None,
             renderer=None,
             wrapper=None):

    config = with_context(_context)
    config.set_notfound_view(view=view, attr=attr, renderer=renderer,
                             wrapper=wrapper)


def forbidden(_context,
             view=None,
             attr=None,
             renderer=None,
             wrapper=None):

    config = with_context(_context)
    config.set_forbidden_view(view=view, attr=attr, renderer=renderer,
                             wrapper=wrapper)

    
class IAssetDirective(Interface):
    """
    Directive for specifying that one package may override assets from
    another package.
    """
    to_override = TextLine(
        title=u"Override spec",
        description=u'The spec of the asset to override.',
        required=True)
    override_with = TextLine(
        title=u"With spec",
        description=u"The spec of the asset providing the override.",
        required=True)

def asset(_context, to_override, override_with, _override=None):
    config = with_context(_context)
    config.override_asset(to_override, override_with, _override=_override)

def set_authentication_policy(config, policy):
    # smooth over differences between pyramid 1.2dev and older
    if hasattr(config, 'set_authentication_policy'): # pragma: no cover
        config.set_authentication_policy(policy)
    else: # pragma: no cover
        config._set_authentication_policy(policy)

class IRepozeWho1AuthenticationPolicyDirective(Interface):
    identifier_name = TextLine(title=u'identitfier_name', required=False,
                               default=u'auth_tkt')
    callback = GlobalObject(title=u'callback', required=False)

def repozewho1authenticationpolicy(_context, identifier_name='auth_tkt',
                                   callback=None):
    policy = RepozeWho1AuthenticationPolicy(identifier_name=identifier_name,
                                            callback=callback)
    # authentication policies must be registered eagerly so they can
    # be found by the view registration machinery
    config = with_context(_context)
    set_authentication_policy(config, policy)

class IRemoteUserAuthenticationPolicyDirective(Interface):
    environ_key = TextLine(title=u'environ_key', required=False,
                           default=u'REMOTE_USER')
    callback = GlobalObject(title=u'callback', required=False)

def remoteuserauthenticationpolicy(_context, environ_key='REMOTE_USER',
                                   callback=None):
    policy = RemoteUserAuthenticationPolicy(environ_key=environ_key,
                                            callback=callback)
    # authentication policies must be registered eagerly so they can
    # be found by the view registration machinery
    config = with_context(_context)
    set_authentication_policy(config, policy)

class IAuthTktAuthenticationPolicyDirective(Interface):
    secret = TextLine(title=u'secret', required=True)
    callback = GlobalObject(title=u'callback', required=False)
    cookie_name = ASCIILine(title=u'cookie_name', required=False,
                            default='auth_tkt')
    secure = Bool(title=u"secure", required=False, default=False)
    include_ip = Bool(title=u"include_ip", required=False, default=False)
    timeout = Int(title=u"timeout", required=False, default=None)
    reissue_time = Int(title=u"reissue_time", required=False, default=None)
    max_age = Int(title=u"max_age", required=False, default=None)
    path = ASCIILine(title=u"path", required=False, default='/')
    http_only = Bool(title=u"http_only", required=False, default=False)
    wild_domain = Bool(title=u"wild_domain", required=False, default=True)

def authtktauthenticationpolicy(_context,
                                secret,
                                callback=None,
                                cookie_name='auth_tkt',
                                secure=False,
                                include_ip=False,
                                timeout=None,
                                reissue_time=None,
                                max_age=None,
                                http_only=False,
                                path='/',
                                wild_domain=True):
    try:
        policy = AuthTktAuthenticationPolicy(secret,
                                             callback=callback,
                                             cookie_name=cookie_name,
                                             secure=secure,
                                             include_ip = include_ip,
                                             timeout = timeout,
                                             reissue_time = reissue_time,
                                             max_age=max_age,
                                             http_only=http_only,
                                             path=path,
                                             wild_domain=wild_domain)
    except ValueError, why: # pragma: no cover
        raise ConfigurationError(str(why))
    # authentication policies must be registered eagerly so they can
    # be found by the view registration machinery
    config = with_context(_context)
    set_authentication_policy(config, policy)

class IACLAuthorizationPolicyDirective(Interface):
    pass

def aclauthorizationpolicy(_context):
    policy = ACLAuthorizationPolicy()
    # authorization policies must be registered eagerly so they can be
    # found by the view registration machinery
    config = with_context(_context)
    if hasattr(config, 'set_authorization_policy'): # pragma: no cover
        # pyramid 1.2dev
        config.set_authorization_policy(policy)
    else: # pragma: no cover
        config._set_authorization_policy(policy)

class IRendererDirective(Interface):
    factory = GlobalObject(
        title=u'IRendererFactory implementation',
        required=True)

    name = TextLine(
        title=u'Token (e.g. ``json``) or filename extension (e.g. ".pt")',
        required=False)

def renderer(_context, factory, name=''):
    # renderer factories must be registered eagerly so they can be
    # found by the view machinery
    config = with_context(_context)
    config.add_renderer(name, factory)

class IStaticDirective(Interface):
    name = TextLine(
        title=u"The URL prefix of the static view",
        description=u"""
        The directory will be served up for the route that starts with
        this prefix.""",
        required=True)

    path = TextLine(
        title=u'Path to the directory which contains assets',
        description=u'May be package-relative by using a colon to '
        'separate package name and path relative to the package directory.',
        required=True)

    cache_max_age = Int(
        title=u"Cache maximum age in seconds",
        required=False,
        default=None)

    permission = TextLine(
        title=u'Permission string',
        description = u'The permission string',
        required = False)

def static(_context, name, path, cache_max_age=3600,
           permission='__no_permission_required__',
           renderer=None):
    """ Handle ``static`` ZCML directives
    """
    config = with_context(_context)
    config.add_static_view(name, path, cache_max_age=cache_max_age,
                           permission=permission, renderer=renderer)

class IScanDirective(Interface):
    package = GlobalObject(
        title=u"The package we'd like to scan.",
        required=True,
        )

def scan(_context, package):
    config = with_context(_context)
    config.scan(package)

class ITranslationDirDirective(Interface):
    dir = TextLine(
        title=u"Add a translation directory",
        description=(u"Add a translation directory"),
        required=True,
        )

def translationdir(_context, dir):
    path = path_spec(_context, dir)
    config = with_context(_context)
    config.add_translation_dirs(path)

class ILocaleNegotiatorDirective(Interface):
    negotiator = GlobalObject(
        title=u"Configure a locale negotiator",
        description=(u'Configure a locale negotiator'),
        required=True,
        )

def localenegotiator(_context, negotiator):
    config = with_context(_context)
    config.set_locale_negotiator(negotiator)

class IAdapterDirective(Interface):
    """
    Register an adapter
    """

    factory = Tokens(
        title=u"Adapter factory/factories",
        description=(u"A list of factories (usually just one) that create"
                     " the adapter instance."),
        required=True,
        value_type=GlobalObject()
        )

    provides  = GlobalInterface(
        title=u"Interface the component provides",
        description=(u"This attribute specifies the interface the adapter"
                     " instance must provide."),
        required=False,
        )

    for_ = Tokens(
        title=u"Specifications to be adapted",
        description=u"This should be a list of interfaces or classes",
        required=False,
        value_type=GlobalObject(
          missing_value=object(),
          ),
        )

    name = TextLine(
        title=u"Name",
        description=(u"Adapters can have names.\n\n"
                     "This attribute allows you to specify the name for"
                     " this adapter."),
        required=False,
        )

def adapter(_context, factory, provides=None, for_=None, name=''):
    if for_ is None:
        if len(factory) == 1:
            for_ = getattr(factory[0], '__component_adapts__', None)

        if for_ is None:
            raise TypeError("No for argument was provided and can't "
                            "determine what the factory adapts.")

    for_ = tuple(for_)

    if provides is None:
        if len(factory) == 1:
            p = list(implementedBy(factory[0]))
            if len(p) == 1:
                provides = p[0]

        if provides is None:
            raise TypeError("Missing 'provided' argument")

    # Generate a single factory from multiple factories:
    factories = factory
    if len(factories) == 1:
        factory = factories[0]
    elif len(factories) < 1:
        raise ValueError("No factory specified")
    elif len(factories) > 1 and len(for_) != 1:
        raise ValueError("Can't use multiple factories and multiple "
                         "for")
    else:
        factory = _rolledUpFactory(factories)
    
    try:
        registry = _context.registry
    except AttributeError: # pragma: no cover (b/c)
        registry = get_current_registry()
        
    _context.action(
        discriminator = ('adapter', for_, provides, name),
        callable = registry.registerAdapter,
        args = (factory, for_, provides, name, _context.info),
        )

class ISubscriberDirective(Interface):
    """
    Register a subscriber
    """

    factory = GlobalObject(
        title=u"Subscriber factory",
        description=u"A factory used to create the subscriber instance.",
        required=False,
        )

    handler = GlobalObject(
        title=u"Handler",
        description=u"A callable object that handles events.",
        required=False,
        )

    provides = GlobalInterface(
        title=u"Interface the component provides",
        description=(u"This attribute specifies the interface the adapter"
                     " instance must provide."),
        required=False,
        )

    for_ = Tokens(
        title=u"Interfaces or classes that this subscriber depends on",
        description=u"This should be a list of interfaces or classes",
        required=False,
        value_type=GlobalObject(
          missing_value = object(),
          ),
        )

def subscriber(_context, for_=None, factory=None, handler=None, provides=None):
    if factory is None:
        if handler is None:
            raise TypeError("No factory or handler provided")
        if provides is not None:
            raise TypeError("Cannot use handler with provides")
        factory = handler
    else:
        if handler is not None:
            raise TypeError("Cannot use handler with factory")
        if provides is None:
            raise TypeError(
                "You must specify a provided interface when registering "
                "a factory")

    if for_ is None:
        for_ = getattr(factory, '__component_adapts__', None)
        if for_ is None:
            raise TypeError("No for attribute was provided and can't "
                            "determine what the factory (or handler) adapts.")

    for_ = tuple(for_)

    config = with_context(_context)

    if handler is not None:
        config.add_subscriber(handler, for_)
    else:
        registry = _context.registry
        _context.action(
            discriminator = None,
            callable = registry.registerSubscriptionAdapter,
            args = (factory, for_, provides, None, _context.info),
            )

class IUtilityDirective(Interface):
    """Register a utility."""

    component = GlobalObject(
        title=u"Component to use",
        description=(u"Python name of the implementation object.  This"
                     " must identify an object in a module using the"
                     " full dotted name.  If specified, the"
                     " ``factory`` field must be left blank."),
        required=False,
        )

    factory = GlobalObject(
        title=u"Factory",
        description=(u"Python name of a factory which can create the"
                     " implementation object.  This must identify an"
                     " object in a module using the full dotted name."
                     " If specified, the ``component`` field must"
                     " be left blank."),
        required=False,
        )

    provides = GlobalInterface(
        title=u"Provided interface",
        description=u"Interface provided by the utility.",
        required=False,
        )

    name = TextLine(
        title=u"Name",
        description=(u"Name of the registration.  This is used by"
                     " application code when locating a utility."),
        required=False,
        )

def utility(_context, provides=None, component=None, factory=None, name=''):
    if factory and component:
        raise TypeError("Can't specify factory and component.")

    if provides is None:
        if factory:
            provides = list(implementedBy(factory))
        else:
            provides = list(providedBy(component))
        if len(provides) == 1:
            provides = provides[0]
        else:
            raise TypeError("Missing 'provides' attribute")

    if factory:
        kw = dict(factory=factory)
    else:
        # older component registries don't accept factory as a kwarg,
        # so if we don't need it, we don't pass it
        kw = {}

    try:
        registry = _context.registry
    except AttributeError: # pragma: no cover (b/c)
        registry = get_current_registry()
        
    _context.action(
        discriminator = ('utility', provides, name),
        callable = registry.registerUtility,
        args = (component, provides, name, _context.info),
        kw = kw,
        )

class IDefaultPermissionDirective(Interface):
    name = TextLine(title=u'name', required=True)

def default_permission(_context, name):
    """ Register a default permission name """
    # the default permission must be registered eagerly so it can
    # be found by the view registration machinery
    config = with_context(_context)
    config.set_default_permission(name)

def path_spec(context, path):
    # we prefer registering asset specifications over absolute
    # paths because these can be overridden by the asset directive.
    if ':' in path and not os.path.isabs(path):
        # it's already an asset specification
        return path
    abspath = context.path(path)
    if hasattr(context, 'package') and context.package:
        return asset_spec_from_abspath(abspath, context.package)
    return abspath

def zcml_configure(name, package):
    """ Given a ZCML filename as ``name`` and a Python package as
    ``package`` which the filename should be relative to, load the
    ZCML into the current ZCML registry.

    """
    registry = get_current_registry()
    configurator = Configurator(registry=registry, package=package)
    configurator.include(includeme)
    configurator.load_zcml(name)
    actions = configurator._ctx.actions[:]
    configurator.commit()
    return actions

file_configure = zcml_configure # backwards compat (>0.8.1)

def _rolledUpFactory(factories):
    def factory(ob):
        for f in factories:
            ob = f(ob)
        return ob
    # Store the original factory for documentation
    factory.factory = factories[0]
    return factory

def with_context(context):
    """Obtain a configurator with 'the right' context.  Returns a new
    Configurator instance."""
    configurator = context.config_class(
        registry=context.registry,
        package=context.package,
        autocommit=context.autocommit,
        )
    configurator.basepath = context.basepath
    configurator.includepath = context.includepath
    configurator.info = context.info
    configurator.route_prefix = context.route_prefix
    configurator.introspection = context.introspection
    if hasattr(configurator, '_make_context'): # pragma: no cover
        # 1.0, 1.1 b/c
        configurator._ctx = context
    return configurator

def load_zcml(self, spec='configure.zcml', lock=threading.Lock()):
    """ Load configuration from a :term:`ZCML` file into the
    current configuration state.  The ``spec`` argument is an
    absolute filename, a relative filename, or a :term:`asset
    specification`, defaulting to ``configure.zcml`` (relative to
    the package of the method's caller)."""
    package_name, filename = self._split_spec(spec)
    if package_name is None: # absolute filename
        package = self.package
    else:
        __import__(package_name)
        package = sys.modules[package_name]

    # To avoid breaking people's expectations of how ZCML works, we
    # cannot autocommit ZCML actions incrementally.  If we commit actions
    # incrementally, configuration outcome will be controlled purely by
    # ZCML directive execution order, which isn't what anyone who uses
    # ZCML expects.  So we don't autocommit each ZCML directive action
    # while parsing is happening, but we do make sure to commit right
    # after parsing if autocommit it True.
    context = ConfigurationMachine()
    context.registry = self.registry
    context.autocommit = False
    context.package = package
    context.route_prefix = getattr(self, 'route_prefix', None)
    context.introspection = getattr(self, 'introspection', True)
    context.config_class = self.__class__
    registerCommonDirectives(context)

    self.manager.push({'registry':self.registry, 'request':None})
    lock.acquire()

    try:
        # old_action_state will be None for Pyramid 1.0 and 1.1, but
        # not for 1.2
        old_action_state = getattr(self.registry, 'action_state', None)
        if old_action_state is not None:
            # For Pyramid 1.2+, we need to assign a temporary action state to
            # the registry, because the configurator actions must populate
            # the context's action list (instead of the registry action
            # state's action list) in order for includeOverrides to work
            # properly.
            from pyramid.config import ActionState 
            self.registry.action_state = ActionState()
            self.registry.action_state.actions = context.actions
        xmlconfig.file(filename, package, context=context, execute=False)
    finally:
        if old_action_state is not None:
            # if we reassigned the action state, restore the old one (1.2 only)
            self.registry.action_state = old_action_state
        lock.release()
        self.manager.pop()

    _ctx = self._ctx
    if _ctx is None: # pragma: no cover ; will never be true under 1.2a5+
        _ctx = self._ctx = self._make_context(self.autocommit)
    _ctx.actions.extend(context.actions)
    if self.autocommit:
        self.commit()

    return self.registry

# note that ``options`` is a b/w compat alias for ``settings`` and
# ``Configurator`` is a testing dep inj
# XXX remove?
def make_app(root_factory, package=None, filename='configure.zcml',
             settings=None, options=None, Configurator=Configurator):
    """ Return a Router object, representing a fully configured
    Pyramid WSGI application.

    .. warning::

       Use of this function is deprecated as of Pyramid 1.0.  You should
       instead use a :class:`pyramid.config.Configurator` instance to perform
       startup configuration as shown in :ref:`configuration_narr`.

    ``root_factory`` must be a callable that accepts a :term:`request`
    object and which returns a traversal root object.  The traversal
    root returned by the root factory is the *default* traversal root;
    it can be overridden on a per-view basis.  ``root_factory`` may be
    ``None``, in which case a 'default default' traversal root is
    used.

    ``package`` is a Python :term:`package` or module representing the
    application's package.  It is optional, defaulting to ``None``.
    ``package`` may be ``None``.  If ``package`` is ``None``, the
    ``filename`` passed or the value in the ``options`` dictionary
    named ``configure_zcml`` must be a) absolute pathname to a
    :term:`ZCML` file that represents the application's configuration
    *or* b) a :term:`asset specification` to a :term:`ZCML` file in
    the form ``dotted.package.name:relative/file/path.zcml``.

    ``filename`` is the filesystem path to a ZCML file (optionally
    relative to the package path) that should be parsed to create the
    application registry.  It defaults to ``configure.zcml``.  It can
    also be a ;term:`asset specification` in the form
    ``dotted_package_name:relative/file/path.zcml``. Note that if any
    value for ``configure_zcml`` is passed within the ``settings``
    dictionary, the value passed as ``filename`` will be ignored,
    replaced with the ``configure_zcml`` value.

    ``settings``, if used, should be a dictionary containing runtime
    settings (e.g. the key/value pairs in an app section of a
    PasteDeploy file), with each key representing the option and the
    key's value representing the specific option value,
    e.g. ``{'reload_templates':True}``.  Note that the keyword
    parameter ``options`` is a backwards compatibility alias for the
    ``settings`` keyword parameter.
    """
    settings = settings or options or {}
    zcml_file = settings.get('configure_zcml', filename)
    config = Configurator(package=package, settings=settings,
                          root_factory=root_factory, autocommit=True)
    config.include(includeme)
    config.hook_zca()
    config.begin()
    config.load_zcml(zcml_file)
    config.end()
    return config.make_wsgi_app()

# includeme function for config.include'ability

def includeme(config):
    """ Function meant to be included via
    :meth:`pyramid.config.Configurator.include`, which sets up the
    Configurator with a ``load_zcml`` method."""
    config.add_directive('load_zcml', load_zcml, action_wrap=False)

