from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import json

def sgn(x):
  return cmp(x, 0)

class UglyRobot(object):

  def __init__(self):
    pass

  def setVelocity(self, x, y):
    print x, y
    y = -y
    leftPower = (y + x - x * y * (sgn(x) + sgn(y)) / 2) * 100
    rightPower = (y - x - x * y * (sgn(x) - sgn(y)) / 2) * 100
    # leftPower = (x - y) * 100
    # rightPower = (-x - y) * 100
    # if rightPower > 100:
    #   print("mod left")
    #   leftPower += (rightPower - 100) / 2
    #   rightPower = 100
    # if leftPower > 100:
    #   print("mod right")
    #   rightPower += (leftPower - 100) / 2
    #   leftPower = 100
    # if leftPower < -100:
    #   leftPower = -(-100 - leftPower) / 2
    print leftPower, rightPower

class UglyGamepadController(object):

  def __init__(self, robot):
    self.robot = robot
    self.state = {}

  def onGamepadState(self, state):
    for k, v in state["state"].iteritems():
      self.state[k] = v
    stickX = self.state.get("LEFT_STICK_X")
    stickY = self.state.get("LEFT_STICK_Y")
    if stickX is not None and stickY is not None:
      self.robot.setVelocity(stickX, stickY)

class UglyProtocol(WebSocketServerProtocol):

  def onGamepadCommand(self, command):
    self.gamepadController.onGamepadState(command)

  def onMessage(self, msg, binary):
    command = json.loads(msg)
    cmd = command.get("cmd")    
    if cmd:
      method = "on" + cmd.capitalize() + "Command"
      try:
        getattr(self, method)(command)
      except AttributeError:
        print("Unknown command received: " + cmd.capitalize)
 
  def onOpen(self):
    self.robot = UglyRobot()
    self.gamepadController = UglyGamepadController(self.robot)

if __name__ == '__main__':

  factory = WebSocketServerFactory("ws://localhost:9000")
  factory.protocol = UglyProtocol
  listenWS(factory)
  reactor.run()
