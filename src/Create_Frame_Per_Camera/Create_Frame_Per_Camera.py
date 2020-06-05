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
        scene = bpy.data.scenes[0]
        camName = cam.name
        marker = scene.timeline_markers.new(camName, frame=i)
        marker.camera = cam


bpy.context.scene.render.resolution_x = 2000
bpy.context.scene.render.resolution_y = 2000

setCameraFrames()    
