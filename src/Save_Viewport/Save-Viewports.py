import bpy
import re
import os

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
                
loc = bpy.context.scene.cursor.location
print(loc)

def setCameraFrames():
    obj_in_scene = bpy.context.scene.collection.all_objects
    cameras = [obj for obj in obj_in_scene if obj.type == 'CAMERA']
    bpy.context.scene.frame_end = len(cameras)

    i = 0;
    for cam in cameras:
        i=i+1
        bpy.context.scene.camera = cam
        scene = bpy.data.scenes['Scene']
        camName = cam.name
        marker = scene.timeline_markers.new(camName, frame=i)
        marker.camera = cam

def saveCameraFrames():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            space.shading.type = 'WIREFRAME'
            space.show_object_viewport_curve = True
            space.show_object_viewport_meta = False
            space.show_object_viewport_font = True
            space.show_object_viewport_surf = False
            space.show_object_viewport_grease_pencil = False
            space.show_object_viewport_armature = False
            space.show_object_viewport_lattice = False
            space.show_object_viewport_empty = False
            space.show_object_viewport_light = False
            space.show_object_viewport_light_probe = False
            space.show_object_viewport_camera = False
            space.show_object_viewport_speaker = False
            
    obj_in_scene = bpy.context.scene.collection.all_objects
    cameras = [obj for obj in obj_in_scene if obj.type == 'CAMERA']
    frameCount = len(cameras)

    i = 0;
    for cam in cameras:
        i=i+1
        bpy.context.scene.camera = cam
        bpy.context.scene.frame_set(i)
        scene = bpy.data.scenes['Scene']
        camName = cam.name
        filePath = "X:\\" + camName + ".png"
        bpy.context.scene.render.filepath = filePath
        bpy.ops.render.opengl(animation=False,write_still=True)
        #bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=filePath, show_multiview=False, use_multiview=False)
        
saveCameraFrames()
bpy.ops.wm.quit_blender()
