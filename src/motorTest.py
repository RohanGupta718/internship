from adafruit_servokit import ServoKit
 
PAN_CHANNEL = 0
TILT_CHANNEL = 1

PAN_PIN = 32
TILT_PIN = 33
PWM_FREQ_HZ = 5

MIN_DUTY = 5.0
MAX_DUTY = 10.0

def angle_to_duty(angle):
    angle = max(0, min(180, angle))
    return MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)

class PanTilt:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PAN_PIN, GPIO.OUT)
        GPIO.setup(TILT_PIN, GPIO.OUT)
 
        self.pan_pwm = GPIO.PWM(PAN_PIN, PWM_FREQ_HZ)
        self.tilt_pwm = GPIO.PWM(TILT_PIN, PWM_FREQ_HZ)
        self.pan_pwm.start(angle_to_duty(90))
        self.tilt_pwm.start(angle_to_duty(90))
 
        self.pan_angle = 90
        self.tilt_angle = 90
 
    def set_angles(self, pan, tilt):
        pan = max(0, min(180, pan))
        tilt = max(0, min(180, tilt))
        self.pan_pwm.ChangeDutyCycle(angle_to_duty(pan))
        self.tilt_pwm.ChangeDutyCycle(angle_to_duty(tilt))
        self.pan_angle = pan
        self.tilt_angle = tilt
 
    def center(self):
        self.set_angles(90, 90)
 
    def cleanup(self):
        self.pan_pwm.stop()
        self.tilt_pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    pt = PanTilt()
    try:
        for angle in [60, 120, 90]:
            print(f"Pan -> {angle}")
            pt.set_angles(angle, 90)
            time.sleep(1)
    finally:
        pt.cleanup()
