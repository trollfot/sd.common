# -*- coding: utf-8 -*-

from five import grok
from sd.common.adapters.storage.interfaces import IDictStorage, IListStorage
from sd.common.fields.annotation import AdapterAnnotationProperty
from zope.annotation.interfaces import IAttributeAnnotatable


class SimpleAnnotationStorage(grok.Adapter):
    """A simple storage system using annotations. It will store the items
    in a list. The key is the index in this list.
    """
    grok.context(IAttributeAnnotatable)
    grok.provides(IListStorage)
    grok.baseclass()

    storage = AdapterAnnotationProperty(
        IListStorage['storage'],
        ns="sd.storage"
        )

    def store(self, obj):
        storage = self.storage
        storage.append(obj)
        self.storage = storage
        return True

    def retrieve(self, key):
        length = len(self.storage)
        if key < length:
            try:
                return self.storage[key].__of__(self.context)
            except IndexError:
                pass
        return False

    def delete(self, key):
        storage = self.storage
        length = len(storage)
        if key < length:
            try:
                del storage[key]
            except IndexError:
                return False
            self.storage = storage
            return True
        return False

    def __getattr__(self, idx):
        return self.retrieve(idx)


class GenericAnnotationStorage(grok.Adapter):
    """A very generic storage system using annotations.
    It will store the items in a dictionnary.
    The key is unique and can be of any hashable type.
    """
    grok.context(IAttributeAnnotatable)
    grok.provides(IDictStorage)
    grok.baseclass()

    storage = AdapterAnnotationProperty(
        IDictStorage['storage'],
        ns="sd.storage"
        )

    def store(self, obj):
        key = obj.name
        storage = self.storage
        if key not in storage.keys():
            storage[key] = obj
            self.storage = storage
            return True
        return False

    def retrieve(self, key):
        item = self.storage.get(key, None)
        if item is None:
            return None
        return self.storage[key].__of__(self.context)

    def delete(self, key):
        storage = self.storage
        if key not in storage.keys():
            return False
        del storage[key]
        self.storage = storage
        return True

    def __getattr__(self, name):
        return self.retrieve(name)
