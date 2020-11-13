import bpy
import json
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



def saveCameraLocations():
    obj_in_scene = bpy.context.scene.collection.all_objects
    cameras = [obj for obj in obj_in_scene if obj.type == 'CAMERA']
    
    data = []
    for cam in cameras:
        #bpy.context.scene.camera = cam
        # Do something else here while this object is the current camera
        print(cam.name)
        print(cam.data.clip_start)
        print(cam.data.clip_end)
        print(bpy.data.objects[cam.name].location)
        print(bpy.data.objects[cam.name].rotation_euler)
        print(cam.data.ortho_scale)

        eul = bpy.data.objects[cam.name].rotation_euler
        obj = {
            "name": cam.name,
            "clip_start": cam.data.clip_start,
            "clip_end": cam.data.clip_end,
            "ortho_scale": cam.data.ortho_scale,
            "location":  (bpy.data.objects[cam.name].location[0],bpy.data.objects[cam.name].location[1],bpy.data.objects[cam.name].location[2],),
            "rotation": (eul[0],eul[1],eul[2])
        }
        data.append(obj)
    filename = bpy.path.basename(bpy.context.blend_data.filepath) + ".json"
     
    filepath = os.path.join(os.path.dirname(bpy.context.blend_data.filepath),filename)
    with open(filepath, 'w') as outfile:
       json.dump(data, outfile)
       
       
def renderViewportAnimation():
    basename = os.path.splitext(bpy.path.basename(bpy.context.blend_data.filepath))[0]
    dirName = 'X:\\Dropbox\\DOCUMENTS\\PROPERTY\\LIVED IN\\5 GOWAR AVENUE\\BUILDING DRAWINGS - PREP\\Document Prep\\Images\\Orthosets\\Orthosets-cabinets\\' + basename
    bpy.context.scene.render.filepath =  dirName + "\\" + basename

    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory " + dirName +  " Created ") 
    except FileExistsError:
        print("Directory " + dirName +  " already exists")

    #bpy.context.space_data.shading.type = 'WIREFRAME'
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

    bpy.ops.render.opengl(animation=True,write_still=True)
    
renderViewportAnimation()
bpy.ops.wm.quit_blender()

#saveCameraLocations()