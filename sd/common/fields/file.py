# -*- coding: utf-8 -*-

from zope import schema
from zope import component
from OFS import Image as ofsimage

_marker = object()

class FileField(schema.Field):

    def __init__(self, **kw):
        super(FileField, self).__init__(**kw)

    def _validate(self, value):
        super(FileField, self)._validate(value)


class FileProperty(object):
    """Stores the given file data in a zodb safe way.
    """

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        value = inst.__dict__.get(self.__name, _marker)
        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)

        return value

    def __set__(self, inst, value):
        name = self.__name
        field = self.__field.bind(inst)
        fields = inst.__dict__
        
        if field.readonly and field.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')

        if value is not None:
            obj = ofsimage.File(name, name, '')
            obj.manage_upload(file=value)
            obj.filename = value.filename
        else:
            obj = None

        fields[name] = obj
        inst._p_changed = True

    def __getattr__(self, name):
        return getattr(self.__field, name)
