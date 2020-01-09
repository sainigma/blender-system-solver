import bpy
import systemSolver as solver

def getSelected(): return bpy.context.selected_objects[0]

def saveToKeyFrames(currentSystem):
  selectedObject = getSelected()
  def saveToKeyframe(state):
    selectedObject.location.z = state.position.y
    frame = int(state.time*framerate)
    selectedObject.keyframe_insert("location",frame=frame)

  framerate = 24
  timeBetweenFrames = 1/framerate
  solver.solveAcceleratingSystem(currentSystem, saveToKeyframe, timeBetweenFrames)