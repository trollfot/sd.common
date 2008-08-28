# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from zope.schema import Dict, Object, List, TextLine
from BTrees.OOBTree import OOBTree


class IStorageItem(Interface):
    """An item that can be stored.
    """
    name = TextLine(
        title=u"name",
        default=u"",
        required=True
        )


class IStorage(Interface):
    """A storage item handles the persistence of a given item.
    A storage has three main actions : store, retrieve, delete.
    """
    storage = Attribute(u"The attribute physically storing the items")

    def store(self, obj):
        """Stores an object and returns True.
        Returns False is the object can't be stored.
        """

    def retrieve(self, key):
        """Retrieve the object according to the given key.
        The retrieving method depends of the storage type.
        If no object is found, None is returned.
        """

    def delete(self, key):
        """Deletes the object with the given oid.
        Returns True if success, False otherwise.
        """


class IListStorage(IStorage):
    """A list storage will store an IStorageItem inside a list.
    The key used during the basic processes is the index in the storage..
    The `store` method will simply append the given item to the existing list.
    Hence, stored items can share the same name.
    """
    storage = List(
        title=u"storage",
        default=[],
        value_type = Object(schema=IStorageItem),
        )


class IDictStorage(IStorage):
    """A dict storage will store an IStorageItem inside a dictionnary.
    The key is the attribute `name` of the stored item. This key is unique in
    the storage. Therefore, stored items can't share the same name.
    """
    storage = Dict(
        title=u"storage",
        default={},
        value_type = Object(schema=IStorageItem),
        )
