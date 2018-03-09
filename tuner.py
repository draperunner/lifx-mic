from math import log2, pow
import mic
from lifxlan import LifxLAN, BLUE, GREEN, RED, YELLOW, PURPLE

A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

lan = LifxLAN()
light = lan.get_lights()

print(light)

tones = {
    "E4": 329.63,
    "B3": 246.94,
    "G3": 196.00,
    "E3": 164.81,
    "D3": 146.83,
    "A2": 110.00,
    "E2": 82.41
}


def pitch(freq):
    h = round(12 * log2(freq / C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


last_tones = []


def tune(frequency, tone="E3"):
    diff = frequency - tones[tone]
    abs_diff = abs(diff)
    if len(last_tones) == 10:
        last_tones.pop(0)
    last_tones.append(abs_diff)
    if len(last_tones) != 10:
        light[0].set_color(RED, rapid=True)
        return

    accumulated_diff = sum(last_tones) / 10
    if accumulated_diff < 5:
        light[0].set_color(GREEN, rapid=True)
    elif accumulated_diff < 15:
        light[0].set_color(YELLOW, rapid=True)
    else:
        light[0].set_color(RED, rapid=True)


mic.listen(tune)
