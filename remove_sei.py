
import argparse
import os

def remove_sei_nals(input_file, output_file, exclude_types=(39, 40)):
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        nal_units = split_nal_units(infile.read())
        for nal in nal_units:
            # SEI NAL units have not excluded type
            if (nal[0] & 0x7E) >> 1 not in exclude_types:
                outfile.write(b'\x00\x00\x01')  # NAL start code
                outfile.write(nal)

def split_nal_units(data):
    nal_units = []
    start_codes = [i for i in range(len(data) - 3) if data[i:i+3] == b'\x00\x00\x01']
    for i in range(len(start_codes) - 1):
        nal_units.append(data[start_codes[i] + 3:start_codes[i + 1]])
    nal_units.append(data[start_codes[-1] + 3:])
    return nal_units

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', nargs='+', type=int, default=(39, 40), help='an integer for the accumulator')
    parser.add_argument('filename', help='input file name')
    args = parser.parse_args()

    exclude_types = tuple(args.t)
    input_file = args.filename

    filename, file_extension = os.path.splitext(input_file)
    output_file = filename + "_no_sei" + file_extension

    remove_sei_nals(input_file, output_file, exclude_types)