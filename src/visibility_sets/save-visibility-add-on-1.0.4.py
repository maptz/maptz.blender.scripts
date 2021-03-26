bl_info = {
    "name": "Move X Axis",
    "blender": (2, 80, 0),
    "category": "Object",
}
#NB For an add-on to appear, Developer extras need to be turned on. 
import bpy
import bpy
import mathutils
import bpy
import math
import re
from bpy.app import handlers
import os
import json


def walk_collection_objects(layer_collection, level = 0, do_func = None):
    for obj in layer_collection.objects:
        cont = do_func(level, obj)
        if cont is True:
            return obj
    for layer in layer_collection.children:
        cont = do_func(level, layer)
        if cont is True:
            return obj
        walk_collection_objects(layer, level +1, do_func)
    return False

def find_collection(layer_collection, predicate, level = 0):
    for layer in layer_collection.children:
        if (predicate(layer, level)):
            return layer
        ret = find_collection(layer, predicate, level + 1)
        if (ret is not None):
            return ret
    return None

def hide_collection(collection, is_hidden = False):
    collection.hide_viewport = is_hidden

def get_collection_visibility(collection_base):
    collection_dict = {}
    def add_collection_to_dict(levl, coll):
        collection_dict[str(levl) + "_" + coll.name] = coll.hide_viewport
    walk_collection_objects(collection_base, do_func=add_collection_to_dict)
    return collection_dict

def set_collection_visibility(collection_base, collection_dict):
    def set_collection_visibility_fn(levl, coll):
        item_name = str(levl) + "_" + coll.name
        if (item_name in collection_dict):
            coll.hide_viewport = collection_dict[item_name]
            coll.hide_render = collection_dict[item_name]
        else:
            coll.hide_viewport = False
            coll.hide_render = False
    print("set_collectio_visibility_called")
    walk_collection_objects(collection_base, do_func=set_collection_visibility_fn)

def get_json_filepath(context):
    if (bpy.data.filepath is None):
            bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)       
    return os.path.splitext(bpy.data.filepath)[0] + ".json"

def load_visibility_props(context):
    dictionary_str = ""
    file_path = get_json_filepath(context)
    if (not os.path.isfile(file_path)):
        return {}
    with open(file_path, "r") as text_file:
        dictionary_str = text_file.read()
    dictionary = json.loads(dictionary_str)
    return dictionary

def save_visibility_props(context, dictionary):
    file_path = get_json_filepath(context)
    dictionary_str = json.dumps(dictionary)
    with open(file_path, "w") as text_file:
        text_file.write(dictionary_str)
    

#Define a proprety type that is used to store the visibility on a scene.
class VisibilityProps(bpy.types.PropertyGroup):
    json_dict = None
    
    def get_items(self, context):
        if (VisibilityProps.json_dict is None):
            VisibilityProps.json_dict = load_visibility_props(context)                
        #NB Because the property is animatable, get_items is called whenever the dropdown is clicked. 
        return [(s, s, s) for s in VisibilityProps.json_dict.keys()]  
    def name_update_func(self, context):
        print("VisibilityProps name updated: " + str(self.name))
    def sets_update_func(self, context):
        print("VisibilityProps groups updated: " + str(self.sets))
        if (self.sets in VisibilityProps.json_dict):
            print("Found. Setting visibilitu.")
            visibility_json = VisibilityProps.json_dict[self.sets]
            visibility_dictionary = json.loads(visibility_json)
            set_collection_visibility(context.scene.collection, visibility_dictionary)
            context.scene.VisibilityProps.name = self.sets
        else:
            print("Not found.")
    
    name : bpy.props.StringProperty(default="", update=name_update_func )
    sets: bpy.props.EnumProperty(items=get_items,  
                                         name = "Visibility sets",  
                                         description = "The visibility sets",
                                         update=sets_update_func,
                                         default=None,
                                         options={'ANIMATABLE'},
                                         get=None,
                                         set=None
                                         )

#Operator used to save visibility when the relevant button is clicked
class SaveVisibilityOperator(bpy.types.Operator):
    bl_idname = "scene.save_visibility_set"   
    bl_label = "Save set"         
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):        
        print("SaveVisibility set executed")
        name = context.scene.VisibilityProps.name
        print("Saving set named " + name)
        #Get the current visibility as a json str
        visibility_dict = get_collection_visibility(context.scene.collection)
        visibility_json_str = json.dumps(visibility_dict)
        if (name in context.scene.VisibilityProps):
            print("Overwriting")
            context.scene.VisibilityProps.json_dict[name] = visibility_json_str
        else:
            print("New")
            context.scene.VisibilityProps.json_dict[name] = visibility_json_str
        save_visibility_props(context, VisibilityProps.json_dict)
        return {'FINISHED'}
    
class SetVisibilityOperator(bpy.types.Operator):
    bl_idname = "scene.set_visibility"   
    bl_label = "Set visibility"         
    bl_options = {'REGISTER', 'UNDO'} 
    
    name: bpy.props.StringProperty()
    
    #call this operator from code with:
    #bpy.ops.scene.set_visibility(name="All")
    def execute(self, context):        
        print("SetVisibility set executed " + self.name)
        context.scene.VisibilityProps.sets = self.name
        return {'FINISHED'}

class DeleteVisibilityOperator(bpy.types.Operator):
    bl_idname = "scene.delete_visibility_set"   
    bl_label = "Delete set"         
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):        
        name = context.scene.VisibilityProps.name
        if (name in context.scene.VisibilityProps.json_dict):
            print("Deleting visibility set " + name)
            del context.scene.VisibilityProps.json_dict[name]
        else:
            print("Visibility set " + name + " not found")
        return {'FINISHED'}

class VisibilityPanel(bpy.types.Panel):
    bl_idname = 'panel.visibility_panel'
    bl_label = 'Visibility'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Visibility'
    # bl_category = "Tools"
    #bl_category = "Panel1"
 
    def draw(self, context):
        layout = self.layout
        layout.label(text= "Visibility sets")
        layout.prop(bpy.context.scene.VisibilityProps, "sets", text="")

        layout.label(text= "Save Visibility set")
        row =layout.row()
        row.prop(bpy.context.scene.VisibilityProps, "name", text="")
        row.operator("scene.save_visibility_set", text = "", icon='PLUS')
        row.operator("scene.delete_visibility_set", text = "", icon='X')

# Register the add-on
classes = [ VisibilityProps, VisibilityPanel, SaveVisibilityOperator, DeleteVisibilityOperator, SetVisibilityOperator ]
def register():
    for cls in classes:
        print("Registering " + str(cls))
        bpy.utils.register_class(cls)
    #Store the VisibilityProps property on objects of type scene.
    bpy.types.Scene.VisibilityProps = bpy.props.PointerProperty(type=VisibilityProps)
def unregister():
    for cls in classes:
        print("Unregistering" + str(cls))
        bpy.utils.unregister_class(cls)
    #Remove the VisibilityProps property on objects of type scene.
    del(bpy.types.Scene.VisibilityProps)
4
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()