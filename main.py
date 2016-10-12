import sys
from os import path
import os

from formats.dat import Dat

if __name__ == "__main__":

    input_dat_path = sys.argv[1]
    base_output_folder = sys.argv[2]
    overwrite = bool(int(sys.argv[2])) if len(sys.argv) > 3 else False

    dat = Dat.open(dat_file_path=input_dat_path)

    for key in dat.keys():

        output_path = path.join(base_output_folder, key)
        output_folder = path.dirname(output_path)

        if not path.exists(output_folder):
            os.makedirs(output_folder)

        output_data = dat[key]
        if not output_data:
            continue

        if not overwrite and path.exists(output_path):
            continue

        with open(output_path, "wb") as output_file:
            print("Writing '%s'..." % output_path)
            output_file.write(output_data)
