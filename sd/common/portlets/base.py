# -*- coding: utf-8 -*-

from plone.app.portlets.portlets import base

class BasePortletRenderer(base.Renderer):
    """A very basic portlet renderer
    """
    def Title(self):
        """Returns the title of the portlet
        """
        return self.data.name
    
