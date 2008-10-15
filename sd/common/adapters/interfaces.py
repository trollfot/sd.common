# -*- coding: utf-8 -*-

from zope.interface import Interface


class IContentQueryHandler(Interface):
    """This interface defines an adapter used in order to fetch the
    very content of a folder-ish type, such as Folder, Topics, etc.
    """
    def query_contents(show_inactive=False, contentFilter=None):
        """
        """
        
