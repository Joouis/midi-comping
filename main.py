import sys
import getopt
from miditoolkit import midi


def digest_midi(midi_path, output_path):
    midi_obj = midi.parser.MidiFile(midi_path)
    lead_track = None
    for track in midi_obj.instruments:
        if track.name == "Lead":
            lead_track = track
    print(midi_obj.instruments)
    assert lead_track != None

    # Only keep lead track now
    midi_obj.instruments = [lead_track]
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
