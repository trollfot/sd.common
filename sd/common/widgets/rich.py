# -*- coding: utf-8 -*-

from zope.app.form.browser.widget import DisplayWidget, renderElement


class RichTextDisplayWidget(DisplayWidget):

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        return renderElement("p", contents=content)
