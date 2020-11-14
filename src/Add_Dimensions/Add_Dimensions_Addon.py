"""Allows you to add dimensions for selected vertices."""
# context.area: VIEW_3D
import mathutils
import bpy
import math
import bmesh
from math import radians
from mathutils import Vector
from .myutils import console_write  # pylint: disable=redefined-builtin
from .myutils import find_collection
from .myutils import make_collection
from .myutils import make_new_collection


def can_calc_bounds():
    """If bounds are calculated, returns True. Otherwise, False."""
    if (bpy.context.object is None):
        return False

    bpy.ops.object.mode_set(mode='OBJECT')
    all_vertices = list(range(0))
    for nr, obj in enumerate(bpy.context.selected_objects):
        if obj.type == 'MESH':
            verts = [v for v in obj.data.vertices if v.select]
            for v in obj.data.vertices:
                if v.select:
                    all_vertices.append(v)
    return len(all_vertices) > 1
    
    # bpy.ops.object.mode_set(mode='OBJECT')
    # mesh = bpy.context.object.data
    # verts = [v for v in mesh.vertices if v.select]
    # return len(verts) > 1


def calc_bounds():
    """Calculates the bounding box for selected vertices.
    Requires applied scale to work correctly. """
    # for some reason we must change into object mode for the calculations
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    all_vertices = list(range(0))
    for nr, obj in enumerate(bpy.context.selected_objects):
        if obj.type == 'MESH':
            for v in obj.data.vertices:
                if v.select:
                    all_vertices.append(v)

    loc = bpy.context.object.location
    # print("Getting verts of boject " + str(loc))

    # mesh = bpy.context.object.data
    # verts = [v for v in mesh.vertices if v.select]
    verts = all_vertices

    if len(verts) <= 1:
        raise Exception("Not enough vertices")
    elif len(verts) == 2:
        bounds = [0, 0, 0, 0, 0, 0]
        bounds[0] = verts[0].co.x
        bounds[1] = verts[1].co.x
        bounds[2] = verts[0].co.y
        bounds[3] = verts[1].co.y
        bounds[4] = verts[0].co.z
        bounds[5] = verts[1].co.z
        bpy.ops.object.mode_set(mode=mode)
        return bounds

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

    # print("Before" + str(bounds))

    bounds[0] = bounds[0] + loc[0]
    bounds[1] = bounds[1] + loc[0]
    bounds[2] = bounds[2] + loc[1]
    bounds[3] = bounds[3] + loc[1]
    bounds[4] = bounds[4] + loc[2]
    bounds[5] = bounds[5] + loc[2]

    # print("After" + str(bounds))

    bpy.ops.object.mode_set(mode=mode)
    return bounds


def saveVertexBounds():
    bounds = calc_bounds()
    # x = bounds[0] - bounds[1]
    # y = (bounds[2] - bounds[3])
    # z = (bounds[4] - bounds[5])
    # strs = "{ \"name: \"" + obj.name + ".part\", \"x\":" + str(x) + ", \"y\":" + str(y) + ", \"z\":" + str(z) + " }"
    # print(strs)
    # bpy.context.window_manager.clipboard = strs


def addLine(fromVertex, toVertex, collection):
    if collection is None:
        collection = bpy.context.scene.collection

    verts = [fromVertex, toVertex]  # 2 verts made with XYZ coords
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    # add a new object using the mesh
    obj = bpy.data.objects.new("Measurement - Line", mesh)

    #    bpy.context.collection.objects.link(obj)  # put the object into the scene (link)
    collection.objects.link(obj)
    if bpy.context.view_layer is None:
        return None

    # set as the active object in the scene
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)  # Select the object

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


def addText(location, name, content, collection, font_size):
    if collection is None:
        collection = bpy.context.scene.collection
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = content
    
    font_curve.size = font_size
    font_curve.align_x = 'CENTER'
    font_obj = bpy.data.objects.new(name, font_curve)
    font_obj.location = location
    collection.objects.link(font_obj)
    bpy.context.view_layer.objects.active = font_obj
    # font_obj.rotation_euler.rotate_axis('X', math.radians(90))
    return font_obj


def addDimensions(plane="xz", offset=1.0, onAxis=True, fontSize=0.2):

    console_write("addDimensions called: '" +
                  plane + "' offset: " + str(offset))

    canDo = can_calc_bounds()
    if (canDo is False):
        return False

    
    # parent_measure_collection = make_collection(
    #     "00 - Measurements", bpy.context.scene.collection)
    measure_collection = make_collection("00 - Measurements", bpy.context.scene.collection)
    # measure_collection = make_collection(
    #     "01 - Measurements - " + plane, parent_measure_collection)
    # measure_collection = make_new_collection("Measurement", measure_collection)
    obj = bpy.context.object
    bounds = calc_bounds()  # TODO With two points, don't calcul    ate bounds.!!
    boundsA = (bounds[0], bounds[2], bounds[4])
    boundsB = (bounds[1], bounds[3], bounds[5])
    # nb bounds1[:] turns this into a tuple
    bounds1 = mathutils.Vector(boundsA)
    bounds2 = mathutils.Vector(boundsB)
    direction = (bounds2 - bounds1)
    direction.normalize()
    # topT.rotation_euler = (radians(0),0,0)
    rotation = (0, 0, 0)

    yvec = mathutils.Vector((0, 1, 0))
    if (plane == "xz"):
        rotation = (radians(90), 0, 0)
        yvec = mathutils.Vector((0, -1, 0))
    if (plane == "xy"):
        rotation = (radians(0), 0, radians(0))
        yvec = mathutils.Vector((0, 0, 1))
    if (plane == "yz"):
        rotation = (radians(90), 0, radians(90))
        yvec = mathutils.Vector((1, 0, 0))

    # crosso sis the cross product with the yvec.
    crosso = direction.copy()
    crosso = crosso.cross(yvec)
    crosso = crosso * offset
    perp = direction.copy()
    perp = perp.cross(yvec)

    dist = (bounds2 - bounds1).length
    textPos = bounds1 + direction * (dist / 2)
    if (onAxis is True):
        if (plane == "xz"):
            textPos[1] = 0
        if (plane == "xy"):
            textPos[2] = 0
        if (plane == "yz"):
            textPos[0] = 0

    # mat_rot = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')
    # textPos = mat_trans * textPos
    textPos = textPos + crosso
    # + crosso * fontSize

    # NB Update viewport to get text height bpy.context.view_layer.update()  https://blender.stackexchange.com/questions/8606/how-do-i-use-python-to-get-the-dimensions-of-a-text-object-immediately-after-it
    dist = round(dist * 1000)
    # addText((0,0,1), str(dist) + "mm")
    text_name = "Measure - Text - " + str(int(round(dist)))
    new_text = addText(textPos, text_name, str(dist), measure_collection, fontSize)
    new_text.rotation_euler = rotation

    lineStart = (bounds1 + crosso)
    lineEnd = (bounds2 + crosso)

    if (onAxis is True):
        if (plane == "xz"):
            lineStart[1] = 0
            lineEnd[1] = 0
        if (plane == "xy"):
            lineStart[2] = 0
            lineEnd[2] = 0
        if (plane == "yz"):
            lineStart[0] = 0
            lineEnd[0] = 0

    new_line = addLine(lineStart[:], lineEnd[:], measure_collection)
    new_line.name = "Measure - Line - " + str(int(round(dist)))

    startTagStart = lineStart
    startTagEnd = lineStart
    tagLen = 0 - offset
    if (plane == "xz"):
        startTagEnd = startTagEnd + perp*tagLen
    if (plane == "xy"):
        startTagEnd = startTagEnd + perp*tagLen
    if (plane == "yz"):
        startTagEnd = startTagEnd + perp*tagLen

    start_tag = addLine(startTagStart[:], startTagEnd[:], measure_collection)

    endTagStart = lineEnd
    endTagEnd = lineEnd
    if (plane == "xz"):
        endTagEnd = endTagEnd + perp*tagLen
    if (plane == "xy"):
        endTagEnd = endTagEnd + perp*tagLen
    if (plane == "yz"):
        endTagEnd = endTagEnd + perp*tagLen

    end_tag = addLine(endTagStart[:], endTagEnd[:], measure_collection)

    join([new_line, start_tag, end_tag])

    new_line.color = (0.0112559, 1, 0.00616773, 1)
    new_text.color = (0.0112559, 1, 0.00616773, 1)

    change_selection = False
    if change_selection:
        obj.select_set(False)  # Select the object
        new_line.select_set(True)  # Select the object
        new_text.select_set(True)  # Select the object
    else:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)  # Select the object
        new_line.select_set(False)  # Select the object
        new_text.select_set(False)  # Select the object

    return True


def join(obs):
    ctx = bpy.context.copy()

    # one of the objects to join
    ctx['active_object'] = obs[0]

    # ctx['selected_objects'] = obs
    # In Blender 2.8x this needs to be the following instead:
    ctx['selected_editable_objects'] = obs

    # We need the scene bases as well for joining.
    # Remove this line in Blender >= 2.80!
    # ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

    bpy.ops.object.join(ctx)

# ------------------------------------------------------------------
# ----ADD ON


if __name__ == "__main__":
    register()

# print("Registered add_dimensions_addon.py")
# addDimensions("xy", -0.3, False)
