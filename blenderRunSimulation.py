import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
import blenderSaveToKeyframe as keyframeSaver

def runCase(caseToRun):
  if caseToRun == 'sinkingSystem' or caseToRun == 'floatingSystem':
    import buoyantCases
    if caseToRun == 'sinkingSystem':
      buoyantCases.createSinkingSystem(keyframeSaver.saveToKeyFrames, None)
    else:
      buoyantCases.createFloatingSystem(keyframeSaver.saveToKeyFrames, None)

runCase('sinkingSystem')