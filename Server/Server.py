from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from Robot import UglyRobot
import json

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
      self.robot.setVelocity(stickX, -stickY)

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
  url = "ws://0.0.0.0:9000"
  factory = WebSocketServerFactory(url)
  factory.protocol = UglyProtocol
  listenWS(factory)
  print("UglyRobot server listening on " + url)
  reactor.run()
