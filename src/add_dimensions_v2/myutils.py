"""Utility functions"""
# myutils.py
import bpy
# pylint: disable=redefined-builtin
def print(data):
    """Prints the data object ot the screen."""
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                # pylint: disable=too-many-function-args
                bpy.ops.console.scrollback_append(override, str(data), "OUTPUT")

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

def find_named_collection(layer_collection, collection_to_find_name):
    """Recursively finds a named layer."""
    found = None
    if layer_collection.name == collection_to_find_name:
        return layer_collection
    for layer in layer_collection.children:
        found = find_named_collection(layer, collection_to_find_name)
        if found:
            return found
