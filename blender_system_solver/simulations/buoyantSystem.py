from blender_system_solver.modules import systemSolver as solver

class buoyantSystem:
  
  state = None
  previousState = None
  useEndPosition = [False, True, False]
  useLinearFill = True
  floating = None

  offsetTime = 0
  endtime = None
  density = None

  accelerating = False
  initialPositionY = None
  fulcrumPositionY = None
  endPosition = solver.cartesianCoordinate()

  timeToFill = None
  initialFillCoefficient = None
  fillCoefficient = None
  finalFillCoefficient = None
  
  siphonForce = 0
  work = 0
  
  progress = 0

  class caseConstants:
    mass = 2440
    outerVolume = 33.2            #m^3
    innerVolume = 38.4            #m^3
    dragCoefficient = 1.05
    dragArea = 14.78              #m^2

  def initialize(self,props):
    self.state = solver.spatialObject()
    self.previousState = solver.spatialObject()

    if 'offsetTime' in props:
      self.offsetTime = props['offsetTime']
    self.endtime = props['endtime']
    self.caseConstants.mass = props['mass']
    self.caseConstants.innerVolume = props['innerVolume']
    self.caseConstants.outerVolume = props['outerVolume']
    self.caseConstants.dragCoefficient = props['dragCoefficient']
    self.caseConstants.dragArea = props['dragArea']
    self.density = props['density']
    self.initialPositionY = props['initialPositionY']
    self.state.position.y = self.initialPositionY
    self.fulcrumPositionY = props['fulcrumPositionY']
    self.endPosition.y = props['endPositionY']
    self.initialFillCoefficient = props['initialFillCoefficient']
    self.finalFillCoefficient = props['finalFillCoefficient']
    self.timeToFill = props['timeToFill']
    if props['endPositionY']<props['initialPositionY']:
      self.floating = False
    else: self.floating = True

  def linearFill(self):
    if self.useLinearFill:
      time = self.state.time
      if time < self.timeToFill:
        linearCoefficient = (self.finalFillCoefficient - self.initialFillCoefficient)/self.timeToFill
        linearPosCoefficient = (self.fulcrumPositionY - self.initialPositionY)/self.timeToFill
        self.fillCoefficient = linearCoefficient*time + self.initialFillCoefficient
        if not self.floating and not self.accelerating:
          self.state.position.y = linearPosCoefficient*time + self.initialPositionY
      else: self.fillCoefficient = self.finalFillCoefficient
    else: self.fillCoefficient = self.finalFillCoefficient

  def acceleration(self):
    if self.useLinearFill:
      self.linearFill()
    forceGravity = -self.caseConstants.mass * solver.systemConstants.gravity
    forceBuyoancy = (self.density * ( self.caseConstants.outerVolume - self.caseConstants.innerVolume * self.fillCoefficient )) * solver.systemConstants.gravity
    forceDrag = solver.dragEquation(self.state.velocity.y, self.caseConstants.dragCoefficient, self.caseConstants.dragArea, self.density)

    if ( self.state.velocity.y > 0 and forceDrag > 0 ) or ( self.state.velocity.y < 0 and forceDrag < 0 ):
      forceDrag *= -1

    netForces = forceGravity + forceBuyoancy + forceDrag
    if self.siphonForce > 0 and (netForces + self.siphonForce) < 0:
      netForces += self.siphonForce
      self.work += self.siphonForce * solver.systemConstants.timestep
    resultAcceleration = solver.cartesianCoordinate()
    resultAcceleration.y = netForces/self.caseConstants.mass

    if netForces > 0 and not self.floating:
      resultAcceleration.y = 0
    elif not self.floating and not self.accelerating:
      self.accelerating = True

    return resultAcceleration

  def endConditionReached(self):
    self.progress = int(100*(1-abs((self.state.position.y - self.endPosition.y)/(self.initialPositionY-self.endPosition.y))))
    if self.floating:
      return (self.useEndPosition[0] and self.state.position.x > self.endPosition.x) or \
        (self.useEndPosition[1] and self.state.position.y > self.endPosition.y) or \
          (self.useEndPosition[2] and self.state.position.z > self.endPosition.z)
    else:
      return (self.useEndPosition[0] and self.state.position.x < self.endPosition.x) or \
        (self.useEndPosition[1] and self.state.position.y < self.endPosition.y) or \
          (self.useEndPosition[2] and self.state.position.z < self.endPosition.z)