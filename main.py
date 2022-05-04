import math
import sys
import getopt
from miditoolkit import midi

# Pitch of drum means tone in MuseScore:
#   Bass(36), Tom(38, 40), Clap(39), Snare(41), Hi-hat(42)

# TODO:
# - Time signature changes handler
# - Expressions:
#   - crescendo/diminuendo, fills/mute
#   - Start to play with bass line
# - 4/4 is too boring
def gen_drum_track(midi_obj):
    beat_res = midi_obj.ticks_per_beat
    print(beat_res)
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

    # print(track.notes)
    return track

def digest_midi(midi_path, output_path):
    midi_obj = midi.parser.MidiFile(midi_path)

    lead_track = None
    for track in midi_obj.instruments:
        if track.name == "Lead":
            lead_track = track
    assert lead_track != None

    print(midi_obj.instruments)
    drum_track = gen_drum_track(midi_obj)

    # Only keep lead track now
    midi_obj.instruments = [lead_track, drum_track]
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
