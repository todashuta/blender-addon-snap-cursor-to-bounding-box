bl_info = {
    "name": "Snap Cursor to Bounding Box",
    "author": "Toda Shuta",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Shift-S (Snap Menu)",
    "description": "Snap Cursor to Bounding Box (Top, Center, Bottom)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


if "bpy" in locals():
    import importlib
    importlib.reload(snap_cursor_to_bounding_box)
else:
    from . import snap_cursor_to_bounding_box


import bpy


def register():
    snap_cursor_to_bounding_box.register()


def unregister():
    snap_cursor_to_bounding_box.unregister()


if __name__ == "__main__":
    register()
