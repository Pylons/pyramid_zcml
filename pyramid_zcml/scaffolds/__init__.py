from pyramid.scaffolds import PyramidTemplate

class StarterZCMLProjectTemplate(PyramidTemplate):
    _template_dir = 'starter_zcml'
    summary = 'pyramid starter project (using ZCML)'
    template_renderer = staticmethod(None)

