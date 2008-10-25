# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts
from zope.app.container.interfaces import IContainer
from zope.cachedescriptors.property import Lazy, CachedProperty

from Acquisition import aq_inner
from AccessControl import getSecurityManager

from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.topic import IATTopic

from base import BaseAdapter
from interfaces import IContentQueryHandler


class FolderishContentQuery(BaseAdapter):
    adapts(IContainer)
    implements(IContentQueryHandler)

    def buildQuery(self, contentFilter):
        if contentFilter.get('path', None) is None:
            contentFilter['path'] = dict(
                query = '/'.join(self.context.getPhysicalPath()),
                depth = 1)

        if contentFilter.get('sort_on', None) is None:
            contentFilter['sort_on'] = "getObjPositionInParent"
        return contentFilter

    @CachedProperty
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @CachedProperty
    def can_query_inactive(self):
        gsm = getSecurityManager()
        return gsm.checkPermission('Access inactive portal content',
                                   aq_inner(self.context))

    def query_contents(self, show_inactive=False, limit=None, **contentFilter):
        """Returns a list of the brains contained in the context.
        """
        show_inactive = show_inactive and self.can_query_inactive
        query = self.buildQuery(contentFilter)        

        if limit and query.get('sort_limit', None) is None:
            query['sort_limit'] = limit
            return self.catalog(show_inactive = show_inactive, **query)[:limit]

        
        return self.catalog(show_inactive = show_inactive, **query)
        

class TopicContentQuery(FolderishContentQuery):
    adapts(IATTopic)
    implements(IContentQueryHandler)

    def buildQuery(self, contentFilter):
        query = self.context.buildQuery()
        for k,v in query.items():
            if contentFilter.has_key(k):
                arg = contentFilter.get(k)
                if (isinstance(arg, (list, tuple)) and
                    isinstance(v, (list, tuple))):
                    contentFilter[k] = [x for x in arg if x in v]
                elif (isinstance(arg, str) and
                      isinstance(v, (list, tuple)) and arg in v):
                    contentFilter[k] = [arg]
                else:
                    contentFilter[k]=v
            else:
                contentFilter[k]=v
        return contentFilter
