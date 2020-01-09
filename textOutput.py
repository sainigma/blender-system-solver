import systemSolver as solver

def outputToConsole(currentSystem):
  def printOutput(state):
    print(currentSystem.state.time, currentSystem.state.position.y)
  solver.solveAcceleratingSystem(currentSystem, printOutput, 1)

def runCase(caseToRun):
  if caseToRun == 'sinkingSystem' or caseToRun == 'floatingSystem':
    import buoyantCases
    if caseToRun == 'sinkingSystem':
      buoyantCases.createSinkingSystem(outputToConsole, None)
    else:
      buoyantCases.createFloatingSystem(outputToConsole, None)

runCase('sinkingSystem')