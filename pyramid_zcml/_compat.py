try:
    u = unicode
except NameError: #pragma NO COVER Py3k
    from html import escape
    PY3 = True
    u = str
    def b(x, encoding='ascii'):
        return bytes(x, encoding)
    def unwrap_func(f):
        return getattr(f, '__func__', f)
else: #pragma NO COVER Python 2
    from cgi import escape
    PY3 = False
    b = str
    def unwrap_func(f):
        return getattr(f, 'im_func', f)
