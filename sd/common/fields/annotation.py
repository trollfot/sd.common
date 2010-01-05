# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree
from zope.annotation.interfaces import IAnnotations
from Acquisition import aq_inner


class AdapterAnnotationProperty(object):
    """Stores the given textual data in an annotation.
    """
    def __init__(self, field, ns=u"sd.common", name=None):
        self._name = name or field.__name__
        self._namespace = ns
        self.__field = field

    def _get_annotation(self, annoted):
        annotation = IAnnotations(aq_inner(annoted))
        namespace  = annotation.get(self._namespace, None)
        if namespace is not None:
            annotation[self._namespace] = OOBTree()
        return annotation[self._namespace]

    def __get__(self, inst, klass):
        field = self.__field.bind(inst)
        annotation = self._get_annotation(inst.context)
        return annotation.get(self._name, field.default)

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        if field.readonly:
            raise ValueError(self._name, 'field is readonly')
        annotation = self._get_annotation(inst.context)
        annotation[self._name] = value

    def __getattr__(self, name):
        return getattr(self.__field, name)
