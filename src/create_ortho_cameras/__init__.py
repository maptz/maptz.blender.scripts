import bpy
from .myutils import console_write
from .myutils import make_new_collection

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


def setFreestyleRender():
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.view_layers["View Layer"].use_pass_combined = False
    bpy.context.scene.view_layers["View Layer"].use_pass_z = False
    bpy.context.scene.view_layers["View Layer"].use_sky = False
    bpy.context.scene.view_layers["View Layer"].use_strand = False
    bpy.context.scene.view_layers["View Layer"].use_ao = False
    bpy.context.scene.view_layers["View Layer"].use_solid = False

    bpy.context.scene.render.use_freestyle = True

    #    bpy.ops.scene.freestyle_lineset_add()

    freestyle_settings = bpy.context.scene.view_layers["View Layer"].freestyle_settings
    lineset = freestyle_settings.linesets.active
    lineset.name = "VisibleLines"
    lineset.linestyle.name = "VisibleLines_LineStyle"
    lineset.linestyle.color = (1.0, 0, 0)

    bpy.ops.scene.freestyle_lineset_add()
    lineset = freestyle_settings.linesets.active
    lineset.name = "HiddenLines"
    lineset.visibility = "HIDDEN"
    lineset.linestyle.name = "HiddenLines_LineStyle"
    lineset.linestyle.color = (0.233016, 0.127577, 0.135271)


def createCamera(orientation, scale, camera_collection):
    console_write("Making camera " + orientation)
    loc = bpy.context.scene.cursor.location
    camera = bpy.data.cameras.new("Camera-Orthogonal-NM")
    camera_obj = bpy.data.objects.new("Camera-Orthogaonl-NM", camera)
    # bpy.ops.object.camera_add(
    #     enter_editmode=False, align='VIEW', location=loc, rotation=(0, 0, 0))

    camera_collection.objects.link(camera_obj)
    camera_obj.location = loc
    camera_obj.rotation_euler = (0,0,0)

    for ob in bpy.context.selected_objects:
        ob.select_set(False)

    bpy.context.view_layer.objects.active = camera_obj
    camera_obj.select_set(True)
    # camera = bpy.context.object
    
    bpy.context.object.data.type = 'ORTHO'
    bpy.context.object.data.ortho_scale = scale
    bpy.context.object.data.show_limits = True
    bpy.context.object.data.clip_start = 1.5
    height = 0

    

    if (orientation == "TOP"):
        bpy.context.object.name = "Camera-Orthogonal-Top"
        console_write("Creating Top Camera")
        bpy.ops.transform.translate(value=(0, 0, scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    if (orientation == "NORTH"):
        bpy.context.object.name = "Camera-Orthogonal-Look-North"
        console_write("Creating North-Looking Camera")
        bpy.ops.transform.translate(value=(0, scale, height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=3.14159, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.context.object.data.clip_end = scale
    if (orientation == "SOUTH"):
        bpy.context.object.name = "Camera-Orthogonal-Look-South"
        console_write("Creating South-Looking Camera")
        bpy.ops.transform.translate(value=(0, -scale, height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.object.data.clip_end = scale
    if (orientation == "WEST"):
        bpy.context.object.name = "Camera-Orthogonal-Look-West"
        console_write("Creating WEST-Looking Camera")
        bpy.ops.transform.translate(value=(-scale, 0.0, height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.object.data.clip_end = scale
    if (orientation == "EAST"):
        bpy.context.object.name = "Camera-Orthogonal-Look-East"
        console_write("Creating East-Looking Camera")
        bpy.ops.transform.translate(value=(scale, 0.0, height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.object.data.clip_end = scale
    
    camera_obj.select_set(False)


def setCameraFrames():
    obj_in_scene = bpy.context.scene.collection.all_objects
    cameras = [obj for obj in obj_in_scene if obj.type == 'CAMERA']
    bpy.context.scene.frame_end = len(cameras)
    i = 0
    for cam in cameras:
        i = i+1
        bpy.context.scene.camera = cam
        scene = bpy.data.scenes['Scene']
        camName = cam.name
        marker = scene.timeline_markers.new(camName, frame=i)
        marker.camera = cam


def createCameras(resolution, scale):
    camera_collection = make_new_collection("Camera-Ortho-Set", bpy.context.collection)

    pixel_width = scale * resolution
    bpy.context.scene.render.resolution_x = pixel_width
    bpy.context.scene.render.resolution_y = pixel_width
    setFreestyleRender()
    createCamera("TOP", scale, camera_collection)
    createCamera("NORTH", scale, camera_collection)
    createCamera("SOUTH", scale, camera_collection)
    createCamera("EAST", scale, camera_collection)
    createCamera("WEST", scale, camera_collection)
    setCameraFrames()
    return True


class CreateOrthoCameras(bpy.types.Operator):
    """Create Ortho Cameras Addon"""
    bl_idname = "create.orthocameras"  # NOTE Must be lowercase
    bl_label = "Create ortho camera set"
    bl_options = {'REGISTER', 'UNDO'}

    resolution: bpy.props.IntProperty(
        name="Resolution (px/m)", default=1000, min=0, max=10000)
    scale: bpy.props.FloatProperty(
        name="Cam Dimension (M)", default=10, min=1, max=100.0)

    def execute(self, context):
        console_write("Running 'CreateOrthoCameras' addon ")
        success = createCameras(self.resolution, self.scale)
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}


classes = [CreateOrthoCameras]
addon_keymaps = []


def menu_func(self, context):
    self.layout.operator(CreateOrthoCameras.bl_idname)


def register():
    # Register the plugin
    wm = bpy.context.window_manager
    # Register the key mao
    km = wm.keyconfigs.addon.keymaps.new(
        name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(CreateOrthoCameras.bl_idname, 'T',
                              'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))
    # Add the menu item
    bpy.types.VIEW3D_MT_object.append(menu_func)
    # register the classes
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    # Unregister all classes
    for i in classes:
        bpy.utils.unregister_class(i)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    # Remove the menu item
    bpy.types.VIEW3D_MT_object.remove(menu_func)
