from blender_system_solver.modules import systemSolver as solver

def outputToConsole(currentSystem):
  def printOutput(state, offsetTime, progress):
    print("time:",currentSystem.state.time+offsetTime,"position:",currentSystem.state.position.y,"progress:",progress)
  solver.solveAcceleratingSystem(currentSystem, printOutput, 1)
  print("Work done by gravity:",currentSystem.workGravity,"Energy lost to drag:",currentSystem.workDrag,"Energy lost, additional:",currentSystem.work)
  print("Acceleration at end:",currentSystem.state.acceleration.y)
def runCase(caseToRun, props):
 if caseToRun == 'buoyantSystem':
    from blender_system_solver.simulations import cases
    cases.createBuoyantSystem(outputToConsole, props)

def runDebug(props):
  if props == None:
    simProps = dict({
              'offsetTime':0,
              'endtime':3600,
              'mass':15000,
              'innerVolume':6,
              'outerVolume':8,
              'dragCoefficient':1.05,
              'dragArea':4,
              'density':997,
              'initialPositionY':0,
              'fulcrumPositionY':-1,
              'endPositionY':-100,
              'initialFillCoefficient':0,
              'finalFillCoefficient':1,
              'timeToFill':2,
              'additionalDragCoefficient':0.5
            })
  else: simProps = props
  runCase('buoyantSystem', simProps)