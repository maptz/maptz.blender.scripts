import mathutils
import bpy
import math
import bmesh
from math import radians
from mathutils import Vector


def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
                
def find_collection(context, item):
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return context.scene.collection

def make_collection(collection_name, parent_collection):
    if collection_name in bpy.data.collections: # Does the collection already exist?
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection) # Add the new collection under a parent
        return new_collection
    
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

def can_calc_bounds():
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    mesh = bpy.context.object.data
    verts = [v for v in mesh.vertices if v.select]
    return len(verts) > 1

def calc_bounds():
    """Calculates the bounding box for selected vertices. Requires applied scale to work correctly. """
    # for some reason we must change into object mode for the calculations
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    loc = bpy.context.object.location
    print("Getting verts of boject " + str(loc))

    mesh = bpy.context.object.data
    verts = [v for v in mesh.vertices if v.select]

    # [+x, -x, +y, -y, +z, -z]
    v = verts[0].co
    bounds = [v.x, v.x, v.y, v.y, v.z, v.z]

    for v in verts:
        if bounds[0] < v.co.x:
            bounds[0] = v.co.x
        if bounds[1] > v.co.x:
            bounds[1] = v.co.x
        if bounds[2] < v.co.y:
            bounds[2] = v.co.y
        if bounds[3] > v.co.y:
            bounds[3] = v.co.y
        if bounds[4] < v.co.z:
            bounds[4] = v.co.z
        if bounds[5] > v.co.z:
            bounds[5] = v.co.z

    print("Before" + str(bounds))

    bounds[0] = bounds[0] + loc[0]
    bounds[1] = bounds[1] + loc[0]
    bounds[2] = bounds[2] + loc[1]
    bounds[3] = bounds[3] + loc[1]
    bounds[4] = bounds[4] + loc[2]
    bounds[5] = bounds[5] + loc[2]    
    
    print("After" + str(bounds))

    bpy.ops.object.mode_set(mode=mode)
    return bounds

def saveVertexBounds():
    obj =  bpy.context.object
    bounds = calc_bounds()
    # x = bounds[0] - bounds[1]
    # y = (bounds[2] - bounds[3])
    # z = (bounds[4] - bounds[5])
    # strs = "{ \"name: \"" + obj.name + ".part\", \"x\":" + str(x) + ", \"y\":" + str(y) + ", \"z\":" + str(z) + " }"
    # print(strs)
    # bpy.context.window_manager.clipboard = strs

def addLine(fromVertex, toVertex, collection=bpy.context.scene.collection):    
    verts = [fromVertex, toVertex]  # 2 verts made with XYZ coords
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    obj = bpy.data.objects.new("Measurement - Line", mesh)  # add a new object using the mesh

    scene = bpy.context.scene
    #    bpy.context.collection.objects.link(obj)  # put the object into the scene (link)
    collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene
    obj.select_set(True) #Select the object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    for v in verts:
        bm.verts.new(v)  # add a new vert

    bm.verts.ensure_lookup_table()
    bm.edges.new((bm.verts[0], bm.verts[1]))

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)  
    bm.free()  # always do this when finishedd
    return obj

def addText(location, str, collection=bpy.context.scene.collection):
    font_curve = bpy.data.curves.new(type="FONT",name="Font Curve")
    font_curve.body = str
    font_curve.size = 0.2
    font_curve.align_x = 'CENTER'
    font_obj = bpy.data.objects.new("Measurement - Font", font_curve)
    font_obj.location = location
    bpy.context.view_layer.objects.active  = font_obj
    #font_obj.rotation_euler.rotate_axis('X', math.radians(90))
    
    collection.objects.link(font_obj)
    return font_obj

def addDimensions(plane="xz", offset=1.0):
    
    canDo = can_calc_bounds()
    if (canDo is False):
        return False
    
    fontSize = 0.2
    measure_collection = make_collection("00 - Measurements", bpy.context.scene.collection)
        
    obj =  bpy.context.object
    bounds = calc_bounds()
    boundsA = (bounds[0],bounds[2],bounds[4])
    boundsB = (bounds[1],bounds[3],bounds[5])
    bounds1 = mathutils.Vector(boundsA) # nb bounds1[:] turns this into a tuple
    bounds2 = mathutils.Vector(boundsB)
    
    direction = (bounds2 - bounds1)
    direction.normalize()
    
    #topT.rotation_euler = (radians(0),0,0)
    rotation = (0,0,0)
    
    yvec = mathutils.Vector((0,1,0))
    if (plane is "xz"):
        rotation = (radians(90),0,0)
        yvec = mathutils.Vector((0,1,0))
    if (plane is "xy"):
        rotation = (radians(0),0,0)
        yvec = mathutils.Vector((0,0,1))
    if (plane is "yz"):
        rotation = (radians(90),0,0)    
        yvec = mathutils.Vector((1,0,0))
    crosso = direction.copy()
    crosso = crosso.cross(yvec)
    crosso = crosso * offset
    
    dist = (bounds2 - bounds1).length
    textPos = bounds1 + direction * (dist / 2)
    #mat_rot = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')
    #textPos = mat_trans * textPos
    textPos = textPos + crosso + crosso * fontSize

    #NB Update viewport to get text height bpy.context.view_layer.update()  https://blender.stackexchange.com/questions/8606/how-do-i-use-python-to-get-the-dimensions-of-a-text-object-immediately-after-it
    dist = round(dist * 1000)
    #addText((0,0,1), str(dist) + "mm")
    new_text = addText(textPos, str(dist), measure_collection)
    new_text.rotation_euler = rotation
        
    lineStart = (bounds1 + crosso)[:]
    lineEnd = (bounds2 + crosso)[:]
    #new_line = addLine(lineStart, lineEnd, measure_collection)
    
    obj.select_set(False) #Select the object
    #new_line.select_set(True) #Select the object
    new_text.select_set(True) #Select the object
    
    return True

class AddDimensionsXYButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "add.dimensionsxy"
    bl_label = "Add dimensions XY"
    bl_options = {'REGISTER', 'UNDO'}
    
    offset: bpy.props.FloatProperty(name="Offset", default=1.0, min=-100.0, max=100.0)
 
    def execute(self, context):
        success = addDimensions("xy", self.offset)
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  
    
class AddDimensionsXZButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "add.dimensionsxz"
    bl_label = "Add dimensions XZ"
    bl_options = {'REGISTER', 'UNDO'}    
    
    offset: bpy.props.FloatProperty(name="Offset", default=1.0, min=-100.0, max=100.0)
 
    def execute(self, context):
        success = addDimensions("xz", self.offset)
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  
class AddDimensionsYZButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "add.dimensionsyz"
    bl_label = "Add dimensions YZ"
    bl_options = {'REGISTER', 'UNDO'}    
    
    offset: bpy.props.FloatProperty(name="Offset", default=1.0, min=-100.0, max=100.0)
 
    def execute(self, context):
        success = addDimensions("yz", self.offset)
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  

classes = [AddDimensionsXYButton, AddDimensionsXZButton, AddDimensionsYZButton]
addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(AddDimensionsXZButton.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))
    
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()