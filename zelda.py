# Tone detection shamelessly stolen from:
# https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/
# !/usr/bin/env python
from time import sleep

import pyaudio
from lifxlan import LifxLAN, BLUE, GREEN, RED, YELLOW, PURPLE
from numpy import zeros, linspace, short, fromstring, hstack, transpose, log
from scipy import fft

lan = LifxLAN()
light = lan.get_lights()

# Bandwidth for detection (i.e., detect frequencies within this margin of error of the TONE)
BANDWIDTH = 7

# Alarm frequencies (Hz) to detect (Use audacity to record a wave and then do Analyze->Plot Spectrum)
note_config = {
    'D4': {
        'base': 298,
        'min': 298 - BANDWIDTH,
        'max': 298 + BANDWIDTH,
        'color': RED
    },
    'E': {
        'base': 330,
        'min': 330 + BANDWIDTH,
        'max': 330 + BANDWIDTH,
        'color': PURPLE
    },
    'G': {
        'base': 192,
        'min': 330 + BANDWIDTH,
        'max': 330 + BANDWIDTH,
        'color': GREEN
    },
    'A': {
        'base': 217,
        'min': 217 - BANDWIDTH - 10,
        'max': 217 + BANDWIDTH,
        'color': YELLOW
    },
    'D5': {
        'base': 147,
        'min': 147 + BANDWIDTH,
        'max': 147 + BANDWIDTH,
        'color': YELLOW
    },
    'B': {
        'base': 250,
        'min': 250 - BANDWIDTH,
        'max': 250 + BANDWIDTH,
        'color': BLUE
    }
}

print(note_config)

freqNow = 1.0
freqPast = 1.0
prevNote = None

# Set up audio sampler
NUM_SAMPLES = 2048
HALF_NUM_SAMPLES = NUM_SAMPLES // 2
SAMPLING_RATE = 44000  # make sure this matches the sampling rate of your mic!
SAMPLING_RATE_DIV_NUM_SAMPLES = SAMPLING_RATE / NUM_SAMPLES

pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

while True:
    while _stream.get_read_available() < NUM_SAMPLES:
        sleep(0.001)
    audio_data = fromstring(_stream.read(
        _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0
    intensity = abs(fft(normalized_data))[:HALF_NUM_SAMPLES]
    frequencies = linspace(0.0, float(SAMPLING_RATE) / 2, num=HALF_NUM_SAMPLES)
    which = intensity[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(intensity) - 1:
        y0, y1, y2 = log(intensity[which - 1:which + 2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        freqPast = freqNow
        freqNow = (which + x1) * SAMPLING_RATE_DIV_NUM_SAMPLES
    else:
        freqNow = which * SAMPLING_RATE / NUM_SAMPLES
        # print("\t\t\t\tfreq=",freqNow,"\t"),freqPast

    if freqNow < 85:
        continue

    # print(freqNow)

    for note, config in note_config.items():
        min_freq = config['min']
        max_freq = config['max']
        color = config['color']

        if prevNote != note and min_freq <= freqPast <= max_freq and min_freq <= freqNow <= max_freq:
            prevNote = note
            light.set_color(color, rapid=True)
            #print("You played", note)
