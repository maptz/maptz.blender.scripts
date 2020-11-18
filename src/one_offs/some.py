import bpy
import re

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

def walk_collections(layer_collection, func, predicate, level = 0):
 for layer in layer_collection.children:
     if (predicate(layer, level)):
        func(layer)
     walk_collections(layer, func, predicate, level + 1)
        

def pred(layer, level):
    return len(layer.children) > 0

def pred2(layer, level):
    prefix = layer.name[:2]
    p = re.compile('^[0-9]+')
    if not p.match(prefix):
        return False
    
    named_level = int(prefix)
    if (named_level != level):
        new_name = str(level +1).zfill(2) + layer.name[2:]
        console_write(layer.name + " -> " + new_name)

def do_something(layer):
    console_write(layer.name)

def create_new_collection():
    my_sub_coll = bpy.data.collections.new("My Sub Collection")
    bpy.context.scene.collection.children.link(my_sub_coll)

walk_collections(bpy.context.scene.collection, do_something, pred2)