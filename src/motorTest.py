import Jetson.GPIO as GPIO
import time

PIN = 32
MIN_PULSE_MS = 0.5
MAX_PULSE_MS = 2.5
STEP_DEGREES = 10        # change this to make steps bigger/smaller
HOLD_TIME = 0.3          # how long to hold the signal at each step

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

def set_angle(angle, duration):
    angle = max(0, min(180, angle))
    pulse_ms = MIN_PULSE_MS + (angle / 180.0) * (MAX_PULSE_MS - MIN_PULSE_MS)
    period_ms = 20.0
    cycles = int(duration * 1000 / period_ms)
    for _ in range(cycles):
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(pulse_ms / 1000)
        GPIO.output(PIN, GPIO.LOW)
        time.sleep((period_ms - pulse_ms) / 1000)

print('Resetting to 0')
set_angle(0, duration=1.0)
time.sleep(1)

for angle in range(0, 181, STEP_DEGREES):
    print(f'Angle -> {angle}')
    set_angle(angle, duration=HOLD_TIME)

GPIO.cleanup()
