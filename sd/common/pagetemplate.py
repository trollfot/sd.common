# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PageTemplates.Expressions import getEngine
from zope.tal.talinterpreter import TALInterpreter
from StringIO import StringIO


class ViewPageTemplateAndMacroFile(ViewPageTemplateFile):
    """This page template class handle to render only a macro in it.
    """

    def renderMacro(self, name, **kwargs):
        """Render the given macro in Python code.
        """

        self._cook_check()
            
        if self._v_errors:
            e = str(self._v_errors)
            return 'Page Template %s has errors: %s' % (self.id, e)
        
        output = StringIO()
        context = self.pt_getContext()
        context.update(kwargs)

        engine = TALInterpreter(self._v_program, self._v_macros,
                                getEngine().getContext(context),
                                output, strictinsert=0)
        engine.interpret(self._v_macros[name])
        return output.getvalue()
