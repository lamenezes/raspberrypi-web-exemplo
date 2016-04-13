"""
Bottle Server to expose the pins of a Raspberry Pi board

Server Routes:
    Mode: /mode/<mode>/<pin>
        <mode> -> input or output
        Example: localhost:8080/mode/output/24

    Input: /<pin>
        Example: localhost:8080/24

    Output: /<pin>/<signal>
        Example: localhost:8080/24/1
"""

from bottle import abort, route, run, template
from rpi import GPIO


GPIO.setup(GPIO.BOARD)


@route('/mode/<mode>/<pin:int>')
def mode(mode, pin):
    MODES = ('input', 'output')
    if mode not in MODES:
        abort(400, 'Wrong mode "%s". It should be %s' % (mode, MODES))
    mode = GPIO.IN if mode == 'input' else GPIO.OUT

    try:
        GPIO.setup(pin, mode)
    except:
        abort(400, 'Invalid pin "%d"' % pin)
    return str(pin)


@route('/<pin:int>')
def input(pin):
    try:
        state = GPIO.input(pin)
    except:
        abort(400, 'Pin "%d" is unset' % pin)
    return str(state)


@route('/<pin:int>/<signal:int>')
def output(pin, signal):
    SIGNALS = (0, 1)
    if signal not in SIGNALS:
        abort(400, 'Invalid signal "%d"' % signal)
    signal = GPIO.HIGH if signal else GPIO.LOW

    try:
        GPIO.output(pin, output)
    except:
        abort(400, 'Could output to pin "%d"' % pin)
    return str(signal)


@route('/')
def home():
    led_pin = 24
    try:
        state = GPIO.input(led_pin)
    except:
        abort(404, 'Could not input from pin "%d"' % led_pin)

    if state == GPIO.HIGH:
        msg = 'ON'
        color = 'green'
    else:
        msg = 'OFF'
        color = 'red'

    return template('The LED is <b style="color: {{color}}">{{msg}}</b>',
                    msg=msg, color=color)


if __name__ == '__main__':
    run(host='localhost', port=8080)
