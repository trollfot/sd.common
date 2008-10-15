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

    @CachedProperty
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @CachedProperty
    def can_query_inactive(self):
        gsm = getSecurityManager()
        return gsm.checkPermission('Access inactive portal content',
                                   aq_inner(self.context))

    def query_contents(self, show_inactive=False, **contentFilter):
        """Returns a list of the brains contained in the context.
        """
        if contentFilter.get('path', None) is None:
            contentFilter['path'] = dict(
                query = '/'.join(self.context.getPhysicalPath()),
                depth = 1)

        if contentFilter.get('sort_on', None) is None:
            contentFilter['sort_on'] = "getObjPositionInParent"
        
        show_inactive = show_inactive and self.can_query_inactive
        return self.catalog(contentFilter, show_inactive = show_inactive)


class TopicContentQuery(FolderishContentQuery):
    adapts(IATTopic)
    implements(IContentQueryHandler)

    @CachedProperty
    def query(self):
        return self.context.buildQuery()

    def merge_filters(self, query, contentFilter):
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

    def query_contents(self, show_inactive=False, **contentFilter):
        """Returns a list of the brains contained in the context.
        """
        query = self.merge_filters(self.query, contentFilter)
        return self.catalog(**query)
        
        

