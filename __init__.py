bl_info = {
    "name": "Snap Cursor to Bounding Box",
    "author": "Toda Shuta",
    "version": (1, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Shift-S (Snap Menu)",
    "description": "Snap Cursor to Bounding Box (Top, Center, Bottom)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


if "bpy" in locals():
    import importlib
    importlib.reload(snapcursortoboundingbox)
else:
    from . import snapcursortoboundingbox


import bpy


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_snap.append(snapcursortoboundingbox.menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_snap.remove(snapcursortoboundingbox.menu_func)


if __name__ == "__main__":
    register()
