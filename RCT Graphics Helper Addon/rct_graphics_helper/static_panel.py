
import bpy
import math
import os

from . render_operator import RCTRender
from . render_task import *

'''
Copyright (c) 2018 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

class RenderStatic(RCTRender, bpy.types.Operator):
    bl_idname = "render.rct_static"
    bl_label = "Render RCT Static"

    scene = None
    props = None

    def execute(self, context):
        self.scene = context.scene
        self.props = self.scene.rct_graphics_helper_static_properties

        self.renderTask = RenderTask(context.scene.rct_graphics_helper_general_properties.out_start_index, context)
        
        for i in range(self.props.number_of_rider_sets + 1):
            self.renderTask.add([[ False, context.scene.rct_graphics_helper_static_properties.viewing_angles, 0, 0, 0 ]], i, False, 0, self.props.number_of_animation_frames)

        return super(RenderStatic, self).execute(context)
        
    def finished(self, context):
        super(RenderStatic, self).finished(context)
        self.report({'INFO'}, 'RCT Static render finished.')

class StaticProperties(bpy.types.PropertyGroup):
    viewing_angles = bpy.props.IntProperty(
        name = "Viewing Angles",
        description = "Number of viewing angles to render for",
        default = 4,
        min = 1)
        
    number_of_rider_sets = bpy.props.IntProperty(
        name = "Rider Sets",
        description = "Number of unqique sets of riders. Usually just the amount of riders for this vehicle. Some rides for example only expect rides in sets of 2 to lower the amount of required graphics. This is often done on vehicles which carry 4 or more riders.",
        default = 0,
        min = 0)
        
    number_of_animation_frames = bpy.props.IntProperty(
        name = "Animation Frames",
        description = "Number of animation frames. For example in use for animated scenery and/or rides.",
        default = 1,
        min = 1)

    
class StaticPanel(bpy.types.Panel):
    bl_label = "RCT Static"
    bl_idname = "RENDER_PT_rct_static"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.rct_graphics_helper_static_properties

        row = layout.row()
        row.prop(properties, "viewing_angles")

        row = layout.row()
        row.prop(properties, "number_of_rider_sets")
        
        row = layout.row()
        row.prop(properties, "number_of_animation_frames")
        
        row = layout.row()
        row.operator("render.rct_static", text = "Render Static Object")

def register_static_panel():
    bpy.types.Scene.rct_graphics_helper_static_properties = bpy.props.PointerProperty(type=StaticProperties)
    
def unregister_static_panel():
    del bpy.types.Scene.rct_graphics_helper_static_properties
