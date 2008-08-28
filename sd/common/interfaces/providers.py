# -*- coding: utf-8 -*-

from zope.schema import TextLine
from Products.ATContentTypes.interface.image import IImageContent

class IImageContentProvider(IImageContent):
    """Provides the image content interface and a simple method to reach
    the image path.
    """
    sub_path = TextLine(title=u'image traverse sub_path')
