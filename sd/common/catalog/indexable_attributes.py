"""This package adds extensions to portal_catalog.
"""
from Acquisition import aq_base
from sd.common.interfaces.providers import IImageContentProvider
from Products.ATContentTypes.interface.image import IImageContent
from Products.ATContentTypes.interface.image import IPhotoAlbumAble
from zope.interface import providedBy


def hasImageAndCaption(object, portal, **kw):
    """This indexable attribute is made to avoid the awakening of the
    object while needing to know if the supposedly attached image exists
    or not. It's very useful for the summary views or other kind of listings.
    """
    object = aq_base(object)

    if (not IImageContent.providedBy(object) and
        not IPhotoAlbumAble.providedBy(object)):
        adapted = IImageContentProvider(object, None)
        if adapted is None:
            return None
        else:
            sub_path = adapted.sub_path
            thumb_path = adapted.thumb_path
            image = adapted.getImage()
    else:
        sub_path = "image"
        thumb_path = "image_"
        image = object.getImage()
    
    if image:
        caption = getattr(object, "getImageCaption", None)
        return {
            'image': True,
            'sub_path': sub_path,
            'thumb_path': thumb_path,
            'caption': caption and caption() or None
            }

    return {'image': False,
            'caption': None,
            'thumb_path': None,
            'sub_path': None}


