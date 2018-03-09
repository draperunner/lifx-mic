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

for note, config in note_config.items():
    min_freq = config['min']
    max_freq = config['max']
    color = config['color']

    if prevNote != note and min_freq <= freqPast <= max_freq and min_freq <= freqNow <= max_freq:
        prevNote = note
        light.set_color(color, rapid=True)
        # print("You played", note)
