import bpy
from .myutils import console_write 

bl_info = {
    "name" : "setup_for_print",
    "author" : "Stephen Ellis",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def setup_for_print():
    bpy.context.space_data.shading.type = 'WIREFRAME'
    bpy.context.space_data.shading.background_type = 'VIEWPORT'
    bpy.context.space_data.shading.background_color = (1, 1, 1)
    bpy.context.space_data.overlay.show_ortho_grid = False
    bpy.context.space_data.overlay.show_floor = False
    bpy.context.space_data.overlay.show_axis_x = False
    bpy.context.space_data.overlay.show_axis_y = False
    bpy.context.space_data.show_object_viewport_light = False
    bpy.context.space_data.show_object_viewport_camera = False
    bpy.context.space_data.show_object_viewport_empty = False
    bpy.context.space_data.shading.xray_alpha_wireframe = 0.45974
    bpy.context.space_data.overlay.show_cursor = False
    bpy.context.space_data.overlay.show_outline_selected = False
    bpy.context.space_data.overlay.show_relationship_lines = False
    bpy.context.space_data.overlay.show_extras = False
    bpy.context.space_data.overlay.show_bones = False
    bpy.context.space_data.overlay.show_motion_paths = False
    #ALSO CAN DO:
    # EDIT / PREFERENCES / INTERFACE / LINE WIDTH = THICK
    #bpy.ops.render.opengl(animation=True)
    return True

class SetupForPrint(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "maptz.setup_for_print" # NOTE Must be lowercase
    bl_label = "Setups screen for protingin"
    bl_options = {'REGISTER', 'UNDO'}

 
    def execute(self, context):
        console_write("Running add on `setup_for_print'")
        success = setup_for_print()
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  


classes = [SetupForPrint]
addon_keymaps = []
def menu_func(self, context):
    self.layout.operator(SetupForPrint.bl_idname)

def register():
    # Register the plugin
    wm = bpy.context.window_manager
    # Register the key mao
    # km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    # kmi = km.keymap_items.new(SetupForPrint.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    # addon_keymaps.append((km, kmi))
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
    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()
    # Remove the menu item
    bpy.types.VIEW3D_MT_object.remove(menu_func)