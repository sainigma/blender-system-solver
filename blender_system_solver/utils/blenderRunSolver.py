import bpy
import sys
import os
from blender_system_solver.modules import systemSolver

def getSelected(): return bpy.context.selected_objects[0]

def runSimulation(currentSystem):
  selectedObject = getSelected()
  wm = bpy.context.window_manager

  def saveToKeyframe(state, offsetTime, progress):
    selectedObject.location.z = state.position.y
    frame = int( ( state.time + offsetTime )*framerate )
    selectedObject.keyframe_insert("location",frame=frame)
    wm.progress_update(progress)

  framerate = 24
  timeBetweenFrames = 1/framerate

  wm.progress_begin(0,100)
  systemSolver.solveAcceleratingSystem(currentSystem, saveToKeyframe, timeBetweenFrames)
  wm.progress_end()

def runCase(caseToRun, props):
 if caseToRun == 'buoyantSystem':
    from blender_system_solver.simulations import cases
    cases.createBuoyantSystem(runSimulation, props)