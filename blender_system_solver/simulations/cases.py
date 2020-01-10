from blender_system_solver.simulations import buoyantSystem

def createBuoyantSystem(outputFunction, props):
  buoyantObject = buoyantSystem.buoyantSystem()
  buoyantObject.initialize(props)
  outputFunction(buoyantObject)