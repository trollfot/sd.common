# -*- coding: utf-8 -*-

from zope.app.form import browser
from zope.app.form.browser import widget
from zope.app.form import interfaces as forminterfaces
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


_marker = object()


class FileWidgetMixin(object):

    @property
    def url(self):
        return '%s/++download++%s' % (
            self.request.get("URL1"),
            self.context.__name__
            )

    @Lazy
    def filename(self):
        filename = getattr(self._data, 'filename', None)
        if filename is None:
            filename = getattr(self._data, '__name__', '')
        return filename


    def __call__(self):
        return widget.renderElement(
            u'a',
            href=self.url,
            contents=self.filename)


class FileDownloadWidget(FileWidgetMixin, browser.DisplayWidget):
    """Widget capable of downloading file.
    """


class FileUploadWidget(FileWidgetMixin, widget.SimpleInputWidget):

    existWidget = ViewPageTemplateFile('templates/exist.pt')
    emptyWidget = ViewPageTemplateFile('templates/empty.pt')

    def __call__(self):

        kwargs = dict(
            name = self.name,
            required = self.context.required,
            modified_name = self._modified_name
            )

        if type(self._data) is not type(_marker):
            download = FileWidgetMixin.__call__(self)
            return download + self.existWidget(**kwargs)

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
