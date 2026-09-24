import Jetson.GPIO as GPIO
import time

PIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

def set_angle(angle, duration=1.0):
    angle = max(0, min(180, angle))
    pulse_ms = 1.0 + (angle / 180.0) * 1.0
    period_ms = 20.0
    cycles = int(duration * 1000 / period_ms)
    for _ in range(cycles):
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(pulse_ms / 1000)
        GPIO.output(PIN, GPIO.LOW)
        time.sleep((period_ms - pulse_ms) / 1000)

print('Resetting to 0')
set_angle(0, duration=1.0)

for angle in [60, 120, 90]:
    print(f'Pan -> {angle}')
    set_angle(angle, duration=1.0)

GPIO.cleanup()
