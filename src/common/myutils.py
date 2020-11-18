"""Utility functions"""
# myutils.py
import bpy
# pylint: disable=redefined-builtin
def console_get():
    for area in bpy.context.screen.areas:
        if area.type == 'CONSOLE':
            for space in area.spaces:
                if space.type == 'CONSOLE':
                    return area, space
    return None, None

def console_write(text):
    area, space = console_get()
    if space is None:
        return

    context = bpy.context.copy()
    context.update(dict(
        space=space,
        area=area,
    ))
    for line in text.split("\n"):
        bpy.ops.console.scrollback_append(context, text=line, type='OUTPUT')

# def print(data):
#     """Prints the data object ot the screen."""
#     console_write(str(data))

def find_collection(context, item):
    """Finds a specific item in the current scene."""
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return context.scene.collection

def make_collection(collection_name, parent_collection):
    """Gets or makes a new collection in the parent collection."""
    if collection_name in bpy.data.collections: # Does the collection already exist?
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection) # Add the new collection under a parent
        return new_collection

def make_new_collection(collection_name, parent_collection):
    """Makes a new collection in the parent collection.
    If a naming collision is detected, a new index is added."""
    index = 0
    currentName = collection_name
    while currentName in bpy.data.collections:
        currentName = collection_name + "." + "{:04n}".format(index)
        index = index + 1

    new_collection = bpy.data.collections.new(currentName)
    parent_collection.children.link(new_collection) # Add the new collection under a parent
    return new_collection

def find_named_collection(layer_collection, collection_to_find_name):
    """Recursively finds a named layer."""
    found = None
    if layer_collection.name == collection_to_find_name:
        return layer_collection
    for layer in layer_collection.children:
        found = find_named_collection(layer, collection_to_find_name)
        if found:
            return found

def walk_collections(layer_collection, predicate, level = 0):
    for layer in layer_collection.children:
        if (predicate(layer, level)):
            return layer
        ret = walk_collections(layer, predicate, level + 1)
        if (ret is not None):
            return ret
    return None

def find_parent_collection(collection_to_find):
    def is_collection_parent(collection, idx):
        for child_coll in collection.children:
            if (child_coll == collection_to_find):
                return True
        return False
    walk_collections(bpy.context.scene.collection, is_collection_parent)
