# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements, Interface
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest


class DownloadTraverser(object):

    implements(ITraversable)
    adapts(Interface, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.response = request.response
        
    def traverse(self, name, ignore):            
        file = getattr(self.context, name, None)
        if file is not None:
            content_type = file.get('content_type', 'application/octet-stream')
            self.response.setHeader('Content-Type', content_type)
            self.response.setHeader('Content-Disposition',
                                    'attachment; filename="%s"' % file.filename)
            return file.__of__(self.context)
        raise NotFound(self.context, name, self.request)
