from modules import systemSolver as solver

def outputToConsole(currentSystem):
  def printOutput(state, offsetTime):
    print("time:",currentSystem.state.time+offsetTime,"position:",currentSystem.state.position.y)
  solver.solveAcceleratingSystem(currentSystem, printOutput, 1)

def runCase(caseToRun, props):
 if caseToRun == 'buoyantSystem':
    from simulations import cases
    cases.createBuoyantSystem(outputToConsole, props)

def runDebug(props):
  if props == None:
    simProps = dict({
              'offsetTime':0,
              'endtime':3600,
              'mass':1000,
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
              'timeToFill':30
            })
  else: simProps = props
  runCase('buoyantSystem', simProps)