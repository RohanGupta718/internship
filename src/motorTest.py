import Jetson.GPIO as GPIO
import time

PIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

def hold_pulse(pulse_ms, duration=1.5):
    period_ms = 20.0
    cycles = int(duration * 1000 / period_ms)
    for _ in range(cycles):
        GPIO.output(PIN, GPIO.HIGH)
        time.sleep(pulse_ms / 1000)
        GPIO.output(PIN, GPIO.LOW)
        time.sleep((period_ms - pulse_ms) / 1000)

print('Enter a pulse width in ms (e.g. 1.5), or q to quit.')
while True:
    val = input('Pulse (ms): ')
    if val.lower() == 'q':
        break
    try:
        hold_pulse(float(val))
    except ValueError:
        print('Enter a number, or q to quit.')

GPIO.cleanup()
