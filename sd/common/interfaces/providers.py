# -*- coding: utf-8 -*-

from zope.interface import Attribute
from Products.ATContentTypes.interface.image import IImageContent


class IImageContentProvider(IImageContent):
    """Provides the image content interface and a simple method to reach
    the image and thumbnails.
    """
    sub_path = Attribute("image traverse sub_path")
    thumb_path = Attribute("thumbnails traverse sub_path."
                           "Scale of the thumb is appened.")
    
