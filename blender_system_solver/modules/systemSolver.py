class systemConstants:
  gravity = 9.80665
  timestep = 0.0001

class cartesianCoordinate:
  x = 0
  y = 0
  z = 0

class spatialObject:
  time=0
  position = cartesianCoordinate()
  velocity = cartesianCoordinate()
  acceleration = cartesianCoordinate()

def dragEquation(velocity, dragCoefficient, dragArea, fluidDensity):
  return fluidDensity*velocity*velocity*dragCoefficient*dragArea/(2)

def solveVelocity(currentVelocity, acceleration, previousAcceleration, timestep):
  def singularVelocity(singularVelocity,singularAcceleration, singularPreviousAcceleration, timestep):
    return singularAcceleration*timestep+(singularAcceleration-singularPreviousAcceleration)*timestep*0.5+singularVelocity

  velocity = cartesianCoordinate()
  velocity.x = singularVelocity(currentVelocity.x, acceleration.x, previousAcceleration.x, timestep)
  velocity.y = singularVelocity(currentVelocity.y, acceleration.y, previousAcceleration.y, timestep)
  velocity.z = singularVelocity(currentVelocity.z, acceleration.z, previousAcceleration.z, timestep)
  return velocity

def solvePosition(currentPosition, velocity, timestep):
  def singularPosition(singularCurrentPosition, singularVelocity, timestep):
    return singularCurrentPosition + singularVelocity*timestep

  position = cartesianCoordinate()
  position.x = singularPosition(currentPosition.x, velocity.x, timestep)
  position.y = singularPosition(currentPosition.y, velocity.y, timestep)
  position.z = singularPosition(currentPosition.z, velocity.z, timestep)
  return position

def solveAcceleratingSystem(currentSystem, executeFunction, executeEveryNthSecond ):
  i=0
  timestep = systemConstants.timestep
  while currentSystem.endConditionReached() == False:
    currentSystem.previousState = currentSystem.state
    currentSystem.state.time += timestep
    currentSystem.state.acceleration = currentSystem.acceleration()
    currentSystem.state.velocity = solveVelocity(currentSystem.state.velocity, currentSystem.state.acceleration, currentSystem.previousState.acceleration, timestep)
    currentSystem.state.position = solvePosition(currentSystem.state.position, currentSystem.state.velocity, timestep)
    if i>=executeEveryNthSecond:
      executeFunction(currentSystem.state, currentSystem.offsetTime, currentSystem.progress)
      i=0
    i+=timestep