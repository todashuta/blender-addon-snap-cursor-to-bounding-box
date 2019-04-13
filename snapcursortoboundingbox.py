import bpy
import numpy as np


def snapCursorToBoudingBox(context, report, *, mode="MIDDLE"):
    vertices = []
    selected_objects = context.selected_objects

    for ob in selected_objects:
        if ob.type == "MESH":
            vertices.extend([ob.matrix_world * v.co for v in ob.data.vertices])
        else:
            report({"WARNING"}, "Ignored Unsupported Object: {}".format(ob.name))

    if len(vertices) == 0:
        return {"CANCELLED"}

    context.scene.cursor_location = (np.max(vertices, axis=0) + np.min(vertices, axis=0)) / 2

    if mode == "TOP":
        context.scene.cursor_location.z = np.max(vertices, axis=0)[2]
    elif mode == "BOTTOM":
        context.scene.cursor_location.z = np.min(vertices, axis=0)[2]


class SnapCursorToBoundingBoxTop(bpy.types.Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_top"
    bl_label = "Snap cursor to the Bounding Box Top of selected item(s)"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        snapCursorToBoudingBox(context, self.report, mode="TOP")
        return {"FINISHED"}


class SnapCursorToBoundingBoxCenter(bpy.types.Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_center"
    bl_label = "Snap cursor to the Bounding Box Center of selected item(s)"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        snapCursorToBoudingBox(context, self.report, mode="MIDDLE")
        return {"FINISHED"}


class SnapCursorToBoundingBoxBottom(bpy.types.Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_bottom"
    bl_label = "Snap cursor to the Bounding Box Bottom of selected item(s)"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        snapCursorToBoudingBox(context, self.report, mode="BOTTOM")
        return {"FINISHED"}


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(SnapCursorToBoundingBoxTop.bl_idname,    text="Cursor to Bounding Box Top")
    layout.operator(SnapCursorToBoundingBoxCenter.bl_idname, text="Cursor to Bounding Box Center")
    layout.operator(SnapCursorToBoundingBoxBottom.bl_idname, text="Cursor to Bounding Box Bottom")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_snap.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_snap.remove(menu_func)


if __name__ == "__main__":
    register()
