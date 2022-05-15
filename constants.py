# normalize pitch if needed
MIN_PITCH = 48
MAX_PITCH = 72
MIDDLE_C = 60

NOTE_PITCHES = {
    'Cb': MIDDLE_C - 1,
    'C': MIDDLE_C,
    'C#': MIDDLE_C + 1,
    'Db': MIDDLE_C + 1,
    'D': MIDDLE_C + 2,
    'D#': MIDDLE_C + 3,
    'Eb': MIDDLE_C + 3,
    'E': MIDDLE_C + 4,
    'E#': MIDDLE_C + 5,
    'F': MIDDLE_C + 5,
    'F#': MIDDLE_C + 6,
    'Gb': MIDDLE_C + 6,
    'G': MIDDLE_C + 7,
    'G#': MIDDLE_C + 8,
    'Ab': MIDDLE_C + 8,
    'A': MIDDLE_C + 9,
    'A#': MIDDLE_C + 10,
    'Bb': MIDDLE_C + 10,
    'B': MIDDLE_C + 11,
    'B#': MIDDLE_C + 12
}

CHORD_TYPE_PITCHES = {
    'm': [0, 3, 7],
    'M': [0, 4, 7],
    '': [0, 4, 7],
    '+': [0, 4, 8],
    'dim': [0, 3, 6],
    'o': [0, 3, 6],
    '7': [0, 4, 7, 10],
    'Mm7': [0, 4, 7, 10],
    '%7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'MM7': [0, 4, 7, 11],
    'm7': [0, 3, 7, 10],
    'mm7': [0, 3, 7, 10],
    'm7b5': [0, 3, 6, 10],
    'dim7': [0, 3, 6, 9],
    'o7': [0, 3, 6, 9]
}