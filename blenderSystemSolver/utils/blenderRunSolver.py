import bpy
import sys
import os

def getSelected(): return bpy.context.selected_objects[0]

def runSimulation(currentSystem):
  selectedObject = getSelected()
  def saveToKeyframe(state, offsetTime):
    selectedObject.location.z = state.position.y
    frame = int( ( state.time + offsetTime )*framerate )
    selectedObject.keyframe_insert("location",frame=frame)

  framerate = 24
  timeBetweenFrames = 1/framerate
  solver.solveAcceleratingSystem(currentSystem, saveToKeyframe, timeBetweenFrames)

def runCase(caseToRun, props):
 if caseToRun == 'buoyantSystem':
    from simulations import cases
    cases.createBuoyantSystem(runSimulation, props)