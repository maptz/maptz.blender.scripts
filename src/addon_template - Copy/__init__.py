import bpy
from .myutils import console_write 

bl_info = {
    "name" : "create_ortho_cameras",
    "author" : "Stephen Ellis",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class MyAddOn(bpy.types.Operator):
    """Defines a button"""
    bl_idname = "command.name" # NOTE Must be lowercase
    bl_label = "command description"
    bl_options = {'REGISTER', 'UNDO'}

    enums = [("op1", "OP1 Description", "xy"),
             ("op2", "OP2 Description", "xz"),
             ("op3", "OP3 Description", "yz")]

    prop1: bpy.props.FloatProperty(name="Offset", default=1.0, min=-100.0, max=100.0)
    prop2: bpy.props.FloatProperty(name="Font Size", default=0.2, min=0.01, max=1.0)
    prop3: bpy.props.EnumProperty(name="Plane", items=enums, default= "op1")
    prop4: bpy.props.BoolProperty(name="On Axis", description="On axis", default=True)
 
    def execute(self, context):
        console_write("Running add on")
        success = True
        if (success is False):
            self.report({"WARNING"}, "Something isn't right")
            return{'CANCELLED'}
        return{'FINISHED'}  


classes = [MyAddOn]
addon_keymaps = []
def menu_func(self, context):
    self.layout.operator(MyAddOn.bl_idname)

def register():
    # Register the plugin
    wm = bpy.context.window_manager
    # Register the key mao
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(MyAddOn.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
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