bl_info = {
    "name": "Snap Cursor to Bounding Box",
    "author": "Toda Shuta",
    "version": (1, 4, 4),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Object Menu > Snap",
    "description": "Snap Cursor to Bounding Box (Top, Center, Bottom)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


import bpy
from bpy.types import (
    Context,
    Object,
    Operator,
    UILayout,
    VIEW3D_MT_add,
    VIEW3D_MT_snap,
)
from mathutils import Vector
import numpy as np



from typing import Literal
OperatorResult = set[Literal[ "RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE" ]]


def get_selected_objects_vertices(context: Context, report) -> list[Vector]:
    vertices = []
    selected_objects = context.selected_objects

    for ob in selected_objects:
        try:
            depsgraph = context.evaluated_depsgraph_get()
            obj_eval = ob.evaluated_get(depsgraph)
            mesh_from_eval = obj_eval.to_mesh()
            vertices.extend([ob.matrix_world @ v.co for v in mesh_from_eval.vertices])
            obj_eval.to_mesh_clear()
        except RuntimeError:
            report({"WARNING"}, f"Unsupported Object: `{ob.name}' [{ob.type}]")

    return vertices


def snapCursorToBoudingBox(context: Context, report, *, mode="MIDDLE") -> OperatorResult:
    vertices = get_selected_objects_vertices(context, report)

    if len(vertices) == 0:
        return {"CANCELLED"}

    context.scene.cursor.location = (np.max(vertices, axis=0) + np.min(vertices, axis=0)) / 2 # type: ignore

    if mode == "TOP":
        context.scene.cursor.location.z = np.max(vertices, axis=0)[2] # type: ignore
    elif mode == "BOTTOM":
        context.scene.cursor.location.z = np.min(vertices, axis=0)[2] # type: ignore

    return {"FINISHED"}


def addBoundingBoxEmptyCube(context: Context, report) -> OperatorResult:
    vertices = get_selected_objects_vertices(context, report)

    if len(vertices) == 0:
        return {"CANCELLED"}

    bbox_empty = bpy.data.objects.new("Bounding Box", None)
    collection = bpy.data.collections.new("Bounding Box Collection")
    context.scene.collection.children.link(collection) # type: ignore
    collection.objects.link(bbox_empty)
    bbox_empty.empty_display_size = 1
    bbox_empty.empty_display_type = "CUBE"
    bbox_empty.location = (np.max(vertices, axis=0) + np.min(vertices, axis=0)) / 2 # type: ignore
    bbox_empty.scale = (np.max(vertices, axis=0) - np.min(vertices, axis=0)) / 2 # type: ignore

    return {"FINISHED"}


def addBoundingBoxMeshCube(context: Context, report) -> OperatorResult:
    vertices = get_selected_objects_vertices(context, report)

    if len(vertices) == 0:
        return {"CANCELLED"}

    location = (np.max(vertices, axis=0) + np.min(vertices, axis=0)) / 2 # type: ignore
    scale = (np.max(vertices, axis=0) - np.min(vertices, axis=0)) # type: ignore
    bpy.ops.mesh.primitive_cube_add(size=1, location=location, scale=scale)
    active_object: Object = context.active_object # type: ignore
    active_object.name = "Bounding Box Mesh"

    return {"FINISHED"}


class AddBoundingBoxEmptyCube(Operator):
    bl_idname = "view3d.add_bounding_box_empty_cube"
    bl_label = "Add Bounding Box Empty Cube of selected item(s)"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return True

    def execute(self, context: Context) -> OperatorResult:
        return addBoundingBoxEmptyCube(context, self.report)


class AddBoundingBoxMeshCube(Operator):
    bl_idname = "view3d.add_bounding_box_mesh_cube"
    bl_label = "Add Bounding Box Mesh Cube of selected item(s)"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return True

    def execute(self, context: Context) -> OperatorResult:
        return addBoundingBoxMeshCube(context, self.report)


class SnapCursorToBoundingBoxTop(Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_top"
    bl_label = "Snap cursor to the Bounding Box Top of selected item(s)"
    bl_description = "Snap cursor to the Bounding Box Top of selected item(s)"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return True

    def execute(self, context: Context) -> OperatorResult:
        return snapCursorToBoudingBox(context, self.report, mode="TOP")


class SnapCursorToBoundingBoxCenter(Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_center"
    bl_label = "Snap cursor to the Bounding Box Center of selected item(s)"
    bl_description = "Snap cursor to the Bounding Box Center of selected item(s)"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return True

    def execute(self, context: Context) -> OperatorResult:
        return snapCursorToBoudingBox(context, self.report, mode="MIDDLE")


class SnapCursorToBoundingBoxBottom(Operator):
    bl_idname = "view3d.snap_cursor_to_bounding_box_bottom"
    bl_label = "Snap cursor to the Bounding Box Bottom of selected item(s)"
    bl_description = "Snap cursor to the Bounding Box Bottom of selected item(s)"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return True

    def execute(self, context: Context) -> OperatorResult:
        return snapCursorToBoudingBox(context, self.report, mode="BOTTOM")


def snap_menu_func(self, context: Context):
    layout: UILayout = self.layout
    layout.separator()
    layout.operator(SnapCursorToBoundingBoxTop.bl_idname,    text="Cursor to Bounding Box Top")
    layout.operator(SnapCursorToBoundingBoxCenter.bl_idname, text="Cursor to Bounding Box Center")
    layout.operator(SnapCursorToBoundingBoxBottom.bl_idname, text="Cursor to Bounding Box Bottom")


def add_menu_func(self, context: Context):
    layout: UILayout = self.layout
    layout.separator()
    layout.operator(AddBoundingBoxEmptyCube.bl_idname, text="Add Bounding Box Empty Cube of selected item(s)", icon="OUTLINER_OB_EMPTY")
    layout.operator(AddBoundingBoxMeshCube.bl_idname,  text="Add Bounding Box Mesh Cube of selected item(s)",  icon="OUTLINER_OB_MESH")


classes = (
        AddBoundingBoxEmptyCube,
        AddBoundingBoxMeshCube,

        SnapCursorToBoundingBoxTop,
        SnapCursorToBoundingBoxCenter,
        SnapCursorToBoundingBoxBottom,
        )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    VIEW3D_MT_snap.append(snap_menu_func)
    VIEW3D_MT_add.append(add_menu_func)


def unregister():
    VIEW3D_MT_snap.remove(snap_menu_func)
    VIEW3D_MT_add.remove(add_menu_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
