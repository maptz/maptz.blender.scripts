# region Imports
import bpy
import math
import mathutils
from .myutils import console_write
# endregion

# region Info
bl_info = {
    "name": "create_ortho_cameras",
    "author": "Stephen Ellis",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}
# endregion

# region Classes


class AddDoorArmature(bpy.types.Operator):
    """Adds a door armature"""
    bl_idname = "add.doorarmature"  # NOTE Must be lowercase
    bl_label = "Add door armature"
    bl_options = {'REGISTER', 'UNDO'}

    enums = [("horizontal", "horizontal", "horizontal"),
             ("vertical", "vertical", "vertical")]

    direction_values = [("clockwise", "clockwise", "clockwise"),
             ("anticlockwise", "anticlockwise", "anticlockwise")]

    orientation: bpy.props.EnumProperty(name="Orientation", items=enums, default="vertical")
    direction: bpy.props.EnumProperty(name="Direction", items=direction_values, default="clockwise")
    # flip: bpy.props.BoolProperty(name="Flip", description="Flip", default=True)
    angle: bpy.props.FloatProperty(
        name="Angle", default=0, min=0, max=360.0)
    scale: bpy.props.FloatProperty(
        name="scale", default=1.0, min=0, max=360.0)

    def execute(self, context):
        console_write("Add door armature called.")
        # add_door_bone()
        flip = True if self.direction == "clockwise" else False
        add_door_bone(self.orientation, flip, self.angle, self.scale)
        success = True
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}


class AddDrawerArmature(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "add.drawerarmature"  # NOTE Must be lowercase
    bl_label = "Add drawer armature"
    bl_options = {'REGISTER', 'UNDO'}

    enums = [("X", "X-Axis", "X"),
             ("Y", "Y-Axis", "Y"),
             ("Z", "Z-Axis", "Z")]

    length: bpy.props.FloatProperty(
        name="Open distance", default=1.0, min=-100.0, max=100.0)
    axis: bpy.props.EnumProperty(name="Axus", items=enums, default="X")
    flip: bpy.props.BoolProperty(name="Flip", description="Flip", default=True)

    def execute(self, context):
        console_write("Add drawer armature")
        add_drawer_bone(self.axis, self.flip, self.length)
        success = True
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}
# endregion


# region Registration
classes = [AddDoorArmature, AddDrawerArmature]
addon_keymaps = []


def add_door_menu_func(self, context):
    self.layout.operator(AddDoorArmature.bl_idname)


def add_drawer_menu_func(self, context):
    self.layout.operator(AddDrawerArmature.bl_idname)


def register():
    # Add the menu item
    bpy.types.VIEW3D_MT_object.append(add_door_menu_func)
    bpy.types.VIEW3D_MT_object.append(add_drawer_menu_func)
    # register the classes
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    # Unregister all classes
    for i in classes:
        bpy.utils.unregister_class(i)
    # Remove the menu item
    bpy.types.VIEW3D_MT_object.remove(add_door_menu_func)
    bpy.types.VIEW3D_MT_object.remove(add_drawer_menu_func)
# endregion


def add_drawer_bone(axis="X", flip=True, length=0.5):
    add_poselib = False
    cursor_location = bpy.context.scene.cursor.location
    bpy.ops.object.armature_add(
        enter_editmode=False, align='WORLD', location=cursor_location, scale=(1, 1, 1))
    armature = bpy.context.view_layer.objects.active

    rna_ui = armature.get('_RNA_UI')
    if rna_ui is None:
        armature['_RNA_UI'] = {}
        rna_ui = armature['_RNA_UI']
    rna_ui["open"] = {"description":"is open",
                  "default": 0.0,
                  "min":0.0,
                  "max":1.0,
                  "soft_min":0.0,
                  "soft_max":1.0}

    armature["open"] = 0.0
    
    angle = -90
    euler_axis = "X"
    if (axis == "Y"):
        euler_axis = "X"
        angle = -90 if flip else 90
    if (axis == "X"):
        euler_axis = "Y"
        angle = -90 if flip else 90
    if (axis == "Z"):
        euler_axis = "X"
        angle = 180 if flip else 0
    armature.rotation_euler.rotate_axis(euler_axis, math.radians(angle))
    bpy.ops.object.transform_apply(rotation=True)

    drawer_open_distance = length

    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.object.pose.bones["Bone"].constraints.new(
        type='LIMIT_LOCATION')
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_min_x = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_min_y = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_min_z = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_max_x = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_max_y = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].use_max_z = True
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].max_y = drawer_open_distance
    bpy.context.object.pose.bones["Bone"].constraints["Limit Location"].owner_space = 'LOCAL'

    if (add_poselib):
        bpy.ops.poselib.new()
        bpy.ops.pose.select_all(action="SELECT")
        bpy.context.object.pose.bones["Bone"].location[1] = bpy.context.object.pose.bones["Bone"].location[1] + drawer_open_distance
        bpy.ops.poselib.pose_add(frame=1, name="Open")
        bpy.ops.pose.select_all(action="SELECT")
        bpy.context.object.pose.bones["Bone"].location[1] = bpy.context.object.pose.bones["Bone"].location[1] - drawer_open_distance
        bpy.ops.poselib.pose_add(frame=2, name="Closed")
        bpy.ops.pose.select_all(action="DESELECT")

    bpy.ops.object.mode_set(mode='OBJECT')
    # Create the driver
    drv = bpy.context.object.pose.bones["Bone"].driver_add('location', 1)
    var = drv.driver.variables.new()
    var.name = 'HelloVar'
    var.type = 'SINGLE_PROP'  # you can use 'SINGLE_PROP', 'LOC_DIFF' or 'ROTATION_DIFF'
    target = var.targets[0]
    target.id = bpy.data.objects.get(armature.name)
    target.data_path = "[\"open\"]"
    drv.driver.expression = str(drawer_open_distance) + ' * %s' % var.name


def add_door_bone(orientation, flip, angle, scale):
    add_poselib = False
    cursor_location = bpy.context.scene.cursor.location
    bpy.ops.object.armature_add(
        enter_editmode=False, align='WORLD', location=cursor_location, scale=(1, 1, 1))
    armature = bpy.context.view_layer.objects.active



    rna_ui = armature.get('_RNA_UI')
    if rna_ui is None:
        armature['_RNA_UI'] = {}
        rna_ui = armature['_RNA_UI']
    rna_ui["open"] = {"description":"is open",
                  "default": 0.0,
                  "min":0.0,
                  "max":1.0,
                  "soft_min":0.0,
                  "soft_max":1.0}

    armature["open"] = 0.0


    # bpy.types.Object.my_prop = bpy.props.FloatProperty(min=0.1, max=10.0, name="my_prop", description="is open")
    # armature.my_prop = 0.3

    armature.scale =  (scale, scale, scale)
    armature.rotation_euler.rotate_axis("Z", math.radians(angle))

    euler_angle = -90
    euler_axis = "X"
    if (orientation == "vertical"):
        euler_axis = "Y"
        euler_angle = -90 if flip else 90
    if (orientation == "horizontal"):
        euler_axis = "X"
        euler_angle = 180 if flip else 0

    armature.rotation_euler.rotate_axis(euler_axis, math.radians(euler_angle))
    bpy.ops.object.transform_apply(rotation=True, location=False)
    
    bpy.ops.object.mode_set(mode='POSE')
    # bpy.context.object.pose.bones["Bone"].constraints.new(
    #     type='LIMIT_ROTATION')
    # bpy.context.object.pose.bones["Bone"].constraints["Limit Rotation"].use_limit_x = True
    # bpy.context.object.pose.bones["Bone"].constraints["Limit Rotation"].use_limit_y = True
    # bpy.context.object.pose.bones["Bone"].constraints["Limit Rotation"].use_limit_z = True
    # bpy.context.object.pose.bones["Bone"].constraints["Limit Rotation"].max_x = 0
    # bpy.context.object.pose.bones["Bone"].constraints["Limit Rotation"].min_x = math.radians(-90)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.object.pose.bones["Bone"].rotation_mode = 'XYZ'
    bpy.context.object.pose.bones["Bone"].rotation_euler.rotate_axis('X', math.radians(0))

    if (add_poselib):
        bpy.ops.poselib.new()
        bpy.context.object.pose.bones["Bone"].rotation_mode = 'XYZ'
        bpy.context.object.pose.bones["Bone"].rotation_euler.rotate_axis(
            'Z', math.radians(-90))

        bpy.ops.pose.select_all(action="SELECT")
        bpy.ops.poselib.pose_add(frame=1, name="Open")
        # bpy.ops.pose.select_all(action="DESELECT")

        bpy.ops.pose.select_all(action="SELECT")
        bpy.context.object.pose.bones["Bone"].rotation_mode = 'XYZ'
        bpy.context.object.pose.bones["Bone"].rotation_euler.rotate_axis(
            'Z', math.radians(+90))  # Rotate it back to 0
        bpy.ops.poselib.pose_add(frame=2, name="Closed")
        bpy.ops.pose.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode='OBJECT')
    # Add the driver
    # NOTE The driver overrides the POSELIB!!!!
    drv = bpy.context.object.pose.bones["Bone"].driver_add('rotation_euler', 0)
    var = drv.driver.variables.new()
    var.name = 'HelloVar'
    var.type = 'SINGLE_PROP'  # you can use 'SINGLE_PROP', 'LOC_DIFF' or 'ROTATION_DIFF'
    target = var.targets[0]
    target.id = bpy.data.objects.get(armature.name)
    target.data_path = "[\"open\"]"
    drv.driver.expression = str(math.radians(-90)) + ' * %s' % var.name

# To apply the pose.
    #bpy.ops.poselib.apply_pose(pose_index=- 1)
