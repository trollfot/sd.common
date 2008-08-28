# -*- coding: utf-8 -*-

from Acquisition import aq_parent, aq_inner, aq_base
from xml.sax import saxutils
from zope.app.form import browser
from zope.app.form.browser import widget
from zope.app.form import interfaces as forminterfaces
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

_marker = object()


class FileUploadWidget(widget.SimpleInputWidget):

    existWidget = ViewPageTemplateFile('templates/exist.pt')
    emptyWidget = ViewPageTemplateFile('templates/empty.pt')

    def __call__(self):
        
        kwargs = dict(
            name = self.name,
            required = self.context.required,
            modified_name = self._modified_name
            )

        if type(self._data) is not type(_marker):
            kwargs['filename'] = self.filename
            return self.existWidget(**kwargs)
            
        return self.emptyWidget(**kwargs)

           
    def _getFormInput(self):
        modify = int(self.request.get('_modify_%s' % self.name, 0))
        if not modify:
            return None
        return self.request.get(self.name, None) or None

    def hasInput(self):
        return (int(self.request.get(self._modified_name, 0)) > 0)

    @Lazy
    def _modified_name(self):
        return "_modify_%s" % self.name

    @Lazy
    def filename(self):
        filename = getattr(self._data, 'filename', None)
        if filename is None:
            filename = getattr(self._data, '__name__', '')
        return filename
