F1 - Blender Start
F1 - Blender Start
https://b3d.interplanety.org/en/using-microsoft-visual-studio-code-as-external-ide-for-writing-blender-scripts-add-ons/#:~:text=Open%20the%20extensions%20panel%20in,Select%20%E2%80%9CBlender%3A%20Start%E2%80%9D.

https://github.com/JacquesLucke/blender_vscode

F1 - Run Script

Execute the Blender: Reload Addons command. For that to work, Blender has to be started using the extension. Your addon does not need to support reloading itself. It only has to have correct register and unregister methods.

To reload the addon every time a file is saved, active the blender.addon.reloadOnSave setting in VS Code.