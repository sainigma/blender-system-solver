debug = False
if debug:
    from debug import textOutput
    textOutput.runDebug(None)
    quit()

bl_info = {
    "name": "System Solver Addon",
    "description": "",
    "author": "Kari Suominen",
    "version": (0, 0, 1),
    "blender": (2, 81, 16),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}
import bpy
from blender_system_solver.utils import blenderRunSolver

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class SimProperties(PropertyGroup):

    startFrame: IntProperty(
      name = "Start frame",
      min = 0,
      max = 360000
    )

    simulationMaxtime: FloatProperty(
      name = "Max simulation time",
      description = "Maximum simulation runtime in seconds",
      default = 3600,
      min = 0,
      max = 3600
    )

    mass: FloatProperty(
      name = "Mass",
      default = 1000,
      min = 1,
      max = 10000
    )

    buoyantDragCoefficient: FloatProperty(
      name = "Drag coefficient",
      default = 1.05,
      min = 0,
      max = 2
    )

    buoyantDragArea: FloatProperty(
      name = "Cross-sectional area for drag",
      default = 4,
      min = 1,
      max = 1000
    )

    buoyantFluidDensity: FloatProperty(
      name = "Fluid density",
      default = 997,
      min = 0.0899,
      max = 13593
    )
    
    outerVolume: FloatProperty(
      name = "Outer volume",
      default = 8,
      min = 1,
      max = 100
    )

    innerVolume: FloatProperty(
      name = "Inner volume",
      default = 6,
      min = 1,
      max = 100
    )

    fulcrumPositionY: FloatProperty(
      name = "Minimum buoyant height",
      description = "Height where the system loses buoyancy",
      default = -1,
      min = -500,
      max = 500
    )

    initialPositionY: FloatProperty(
      name = "Initial position",
      default = 0,
      min = -1500,
      max = 1500
    )

    endPositionY: FloatProperty(
      name = "End height",
      description = "End condition for height in meters",
      default = -100,
      min = -5000,
      max = 5000
    )

    initialFill: FloatProperty(
      name = "Initial fill percentage",
      default = 0,
      min = 0,
      max = 1
    )

    finalFill: FloatProperty(
      name = "Final fill percentage",
      default = 1,
      min = 0,
      max = 1
    )

    timeToFill: FloatProperty(
      name = "Time to fill",
      default = 30,
      min = 0,
      max = 240,
      subtype = "TIME"
    )

    simulationType: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('buoyantSystem', "Buoyant System", ""),
                ('ballistics', "Ballistics", ""),
               ]
        )


class WM_OT_ReverseBuoyantSimulation(Operator):
  bl_label = "Reverse variables"
  bl_idname = "wm.run_buoyant_reverse"

  def execute(self,context):
    scene = context.scene
    mytool = scene.my_tool

    oldEndPositionY = mytool.endPositionY
    mytool.endPositionY = mytool.initialPositionY
    mytool.initialPositionY = oldEndPositionY

    oldFinalFill = mytool.finalFill
    mytool.finalFill = mytool.initialFill
    mytool.initialFill = oldFinalFill

    return {'FINISHED'}

class WM_OT_RunBuoyantSimulation(Operator):
    bl_label = "Run buoyancy simulation"
    bl_idname = "wm.run_buoyantsimulation"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        currentObject = bpy.context.selected_objects[0]
        bpy.context.scene.frame_set(mytool.startFrame)
        offsetTime = (1/bpy.context.scene.render.fps)*mytool.startFrame

        simProps = dict({
          'offsetTime':offsetTime,
          'endtime':mytool.simulationMaxtime,
          'mass':mytool.mass,
          'innerVolume':mytool.innerVolume,
          'outerVolume':mytool.outerVolume,
          'dragCoefficient':mytool.buoyantDragCoefficient,
          'dragArea':mytool.buoyantDragArea,
          'density':mytool.buoyantFluidDensity,
          'initialPositionY':mytool.initialPositionY,
          'fulcrumPositionY':mytool.fulcrumPositionY,
          'endPositionY':mytool.endPositionY,
          'initialFillCoefficient':mytool.initialFill,
          'finalFillCoefficient':mytool.finalFill,
          'timeToFill':mytool.timeToFill
        })

        blenderRunSolver.runCase(mytool.simulationType, simProps)
        return {'FINISHED'}

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "System Solver"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "System Solver"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        if len(bpy.context.selected_objects)==1:
          currentObject = bpy.context.selected_objects[0]
          layout.prop(mytool, "simulationType", text="") 
          layout.prop(mytool, "startFrame")
          layout.prop(mytool, "simulationMaxtime")
          if mytool.simulationType == 'buoyantSystem':
            layout.label(text="Constants:")
            layout.prop(mytool, "mass")
            layout.separator()
            layout.prop(mytool, "innerVolume")
            layout.prop(mytool, "outerVolume")
            layout.separator()
            layout.prop(mytool, "buoyantDragCoefficient")
            layout.prop(mytool, "buoyantDragArea")
            layout.prop(mytool, "buoyantFluidDensity")
            layout.separator()

            layout.label(text="Height:")
            layout.prop(mytool, "fulcrumPositionY")
            layout.prop(mytool, "initialPositionY")
            layout.prop(mytool, "endPositionY")
            layout.separator()
            
            layout.label(text="Fill settings")
            layout.prop(mytool, "initialFill")
            layout.prop(mytool, "finalFill")
            layout.prop(mytool, "timeToFill")
            layout.separator()
          layout.operator("wm.run_buoyant_reverse")
          layout.operator("wm.run_buoyantsimulation")

classes = (
    SimProperties,
    WM_OT_ReverseBuoyantSimulation,
    WM_OT_RunBuoyantSimulation,
    OBJECT_PT_CustomPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=SimProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()