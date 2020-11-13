import bpy
import re
import os
from .myutils import console_write 

bl_info = {
    "name" : "create_frame_per_camera",
    "author" : "Stephen Ellis",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


def setCameraFrames():
    obj_in_scene = bpy.context.scene.collection.all_objects
    cameras = [obj for obj in obj_in_scene if obj.type == 'CAMERA']
    bpy.context.scene.frame_end = len(cameras)

    i = 0
    for cam in cameras:
        i=i+1
        bpy.context.scene.camera = cam
        scene = bpy.data.scenes[0]
        camName = cam.name
        marker = scene.timeline_markers.new(camName, frame=i)
        marker.camera = cam
    return True


class CreateFramePerCamera(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "create.frame_per_camera" # NOTE Must be lowercase
    bl_label = "Creates a frame per camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        console_write("Create frame per camera")
        success = setCameraFrames()
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  

classes = [CreateFramePerCamera]
addon_keymaps = []
def menu_func(self, context):
    self.layout.operator(CreateFramePerCamera.bl_idname)

def register():
    # Register the plugin
    wm = bpy.context.window_manager
    # Register the key mao
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(CreateFramePerCamera.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))
    # Add the menu item
    bpy.types.VIEW3D_MT_object.append(menu_func)
    # register the classes
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    #Unregister all classes
    for i in classes:
        bpy.utils.unregister_class(i)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    # Remove the menu item
    bpy.types.VIEW3D_MT_object.remove(menu_func)