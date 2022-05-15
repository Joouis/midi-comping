import sys
import getopt
from miditoolkit import midi
from constants import NOTE_PITCHES, CHORD_TYPE_PITCHES

# Pitch of drum means tone in MuseScore:
#   Bass(36), Tom(38, 40), Clap(39), Snare(41), Hi-hat(42)

# TODO:
# - Expressions:
#   - crescendo/diminuendo, fills/mute
#   - Start to play with bass line
# - 4/4 is too boring
def gen_drum_track(midi_obj):
    beat_res = midi_obj.ticks_per_beat
    # Program means tone?
    track = midi.containers.Instrument(program=1, is_drum=True, name="Basic percussion")
    for idx, tc in enumerate(midi_obj.tempo_changes):
        tempo = round(tc.tempo)
        # Tempo need to be in range [0, 127], why?
        tempo = 127 if tempo > 127 else tempo
        start_time = round(tc.time)
        end_time = round(midi_obj.tempo_changes[idx + 1].time) if idx + 1 < len(midi_obj.tempo_changes) else midi_obj.max_tick
        start = start_time
        duration = round(beat_res * 0.5)
        end = start + duration
        beat_count = 1

        # This way can't handle complicated rhythmic pattern
        while start < end_time:
            if end >= end_time:
                end = end_time
            if beat_count == 4:
                beat_count = 1
                pitch = 42
            else:
                if beat_count == 1:
                    pitch = 36
                elif beat_count == 2:
                    pitch = 42
                else:
                    pitch = 38
                beat_count += 1

            note = midi.containers.Note(start=start, end=end, velocity=tempo, pitch=pitch)
            track.notes.append(note)
            start = start + beat_res
            end = start + duration

    return track


def tempos_markers_handler(midi_obj, cb):
    for idx, tc in enumerate(midi_obj.tempo_changes):
        # TODO: duplicate from gen_drum_track, move it to a util func later
        tempo = round(tc.tempo)
        # Tempo need to be in range [0, 127], why?
        tempo = 127 if tempo > 127 else tempo
        tempo_start_time = round(tc.time)
        tempo_end_time = round(midi_obj.tempo_changes[idx + 1].time) if idx + 1 < len(midi_obj.tempo_changes) else midi_obj.max_tick

        for idx, marker in enumerate(midi_obj.markers):
            chord_start_time = round(marker.time)
            chord_end_time = round(midi_obj.markers[idx + 1].time) if idx + 1 < len(midi_obj.markers) else midi_obj.max_tick
            if chord_start_time >= chord_end_time or chord_end_time < tempo_start_time or chord_start_time > tempo_end_time:
                continue

            # Current tempo in the period
            chord_start_time = tempo_start_time if chord_start_time < tempo_start_time else chord_start_time
            chord_end_time = tempo_end_time if tempo_end_time < chord_end_time else chord_end_time

            [root_note, chord_type] = marker.text.split('_')
            if root_note is None or chord_type is None or root_note not in NOTE_PITCHES or chord_type not in CHORD_TYPE_PITCHES:
                print(f'Unrecognized note {root_note} or chord type {chord_type}')
                continue

            cb(tempo, root_note, chord_type, chord_start_time, chord_end_time)


def get_bass_track(midi_obj):
    beat_res = midi_obj.ticks_per_beat
    track = midi.containers.Instrument(program=33, is_drum=False, name="Bass")

    def note_gen(tempo, root_note, chord_type, chord_start_time, chord_end_time):
        base_pitch = NOTE_PITCHES[root_note]

        start = chord_start_time
        duration = round(beat_res * 0.5)
        end = start + duration
        beat_count = 1

        while start < chord_end_time:
            if end >= chord_end_time:
                end = chord_end_time
            beat_count = 1 if beat_count == 4 else beat_count + 1

            if beat_count == 1 or beat_count == 3:
                pitch = base_pitch - 24
                note = midi.containers.Note(start=start, end=end, velocity=tempo, pitch=pitch)
                track.notes.append(note)

            start = start + beat_res
            end = start + duration
    
    tempos_markers_handler(midi_obj, note_gen)
    return track


def get_piano_track(midi_obj):
    beat_res = midi_obj.ticks_per_beat
    track = midi.containers.Instrument(program=1, is_drum=False, name="Piano")

    def note_gen(tempo, root_note, chord_type, chord_start_time, chord_end_time):
        base_pitch = NOTE_PITCHES[root_note]
        chord_pitches = CHORD_TYPE_PITCHES[chord_type]
        chord_note_num = len(chord_pitches)

        start = chord_start_time
        duration = round(beat_res)
        end = start + duration
        chord_note_idx = 0
        step = 1

        while start < chord_end_time:
            if end >= chord_end_time:
                end = chord_end_time
            if chord_note_idx == chord_note_num - 1:
                step = -1
            elif chord_note_idx == -1:
                chord_note_idx = 1
                step = 1

            pitch = base_pitch + chord_pitches[chord_note_idx]
            note = midi.containers.Note(start=start, end=end, velocity=tempo, pitch=pitch)
            track.notes.append(note)
            start = start + beat_res
            end = start + duration
            chord_note_idx += step

    tempos_markers_handler(midi_obj, note_gen)
    return track


def digest_midi(midi_path, output_path):
    midi_obj = midi.parser.MidiFile(midi_path)

    lead_track = None
    for track in midi_obj.instruments:
        if track.name == "Lead":
            lead_track = track
    assert lead_track != None

    print(midi_obj.instruments)

    # TODO: make instruments optional or simple/middle level
    drum_track = gen_drum_track(midi_obj)
    bass_track = get_bass_track(midi_obj)
    piano_track = get_piano_track(midi_obj)

    # Only keep lead track now
    midi_obj.instruments = [lead_track, drum_track, bass_track, piano_track]
    midi_obj.dump(output_path)
    print(f'Output file: {output_path}')


def main(argv):
    input_path = ''
    output_path = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_path> -o <output_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_path> -o <output_path>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_path = arg
        elif opt in ("-o", "--ofile"):
            output_path = arg
    print(f'Input file: {input_path}')
    # print(f'Output file: {output_path}')

    if input_path and output_path:
        digest_midi(input_path, output_path)

if __name__ == "__main__":
    main(sys.argv[1:])
