import bpy
from .add_dimensions_addon import addDimensions
from .myutils import console_write

bl_info = {
    "name" : "add_dimensions",
    "author" : "Stephen Ellis",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class AddDimensionsButton(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "add.dimensions"
    bl_label = "Add dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    planes = [("xy", "XY", "xy"),
             ("xz", "XZ", "xz"),
             ("yz", "YZ", "yz")]

    
    offset: bpy.props.FloatProperty(name="Offset", default=1.0, min=-100.0, max=100.0)
    font_size: bpy.props.FloatProperty(name="Font Size", default=0.2, min=0.01, max=1.0)
    plane: bpy.props.EnumProperty(name="Plane", items=planes, default= "xy")
    on_axis: bpy.props.BoolProperty(name="On Axis", description="On axis", default=True)
 
    def execute(self, context):
        pl = str(self.plane)
        pri = "Axis " + pl + " offset " + str(self.offset)
        #console_write(pri)
        success = addDimensions(str(pl), self.offset, self.on_axis, self.font_size)
        #success = addDimensions("xy", self.offset)
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  


classes = [AddDimensionsButton]
addon_keymaps = []
def menu_func(self, context):
    self.layout.operator(AddDimensionsButton.bl_idname)

def register():
    # Register the plugin
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(AddDimensionsButton.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))

    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    for i in classes:
        bpy.utils.register_class(i)


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.VIEW3D_MT_object.remove(menu_func)
