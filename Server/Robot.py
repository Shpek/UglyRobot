from Adafruit_PWM_Servo_Driver import PWM

SERVO_ZONES = \
[ [ 330, 400, 405, 475  ], \
  [ 317, 392, 398, 473 ] ]

def sgn(x):
  return cmp(x, 0)

class UglyRobot(object):

  def __init__(self):
    self.pwm = PWM(0x40)
    self.pwm.setPWMFreq(60)

  def setPowerToServo(self, servo, power):
    zone = SERVO_ZONES[servo]
    if abs(power) < 0.0001:
      pwmValue = 0
    elif power > 0:
      pwmValue = zone[1] - power * (zone[1] - zone[0])
    elif power < 0:
      pwmValue = zone[2] - power * (zone[3] - zone[2])
    self.pwm.setPWM(servo, 0, int(pwmValue))

  def setVelocity(self, x, y):
    leftPower = (y + x - x * y * (sgn(x) + sgn(y)) / 2)
    rightPower = (y - x - x * y * (sgn(x) - sgn(y)) / 2)
    leftPower *= leftPower
    rightPower *= rightPower
    self.setPowerToServo(0, leftPower)
    self.setPowerToServo(1, -rightPower)
