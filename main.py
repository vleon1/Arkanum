# import sys
# from os import path
# import os
#
# from formats.dat import Dat
#
# if __name__ == "__main__":
#
#     input_dat_path = sys.argv[1]
#     base_output_folder = sys.argv[2]
#     overwrite = bool(int(sys.argv[2])) if len(sys.argv) > 3 else False
#
#     dat = Dat.open(dat_file_path=input_dat_path)
#
#     for key in dat.keys():
#
#         output_path = path.join(base_output_folder, key)
#         output_folder = path.dirname(output_path)
#
#         if not path.exists(output_folder):
#             os.makedirs(output_folder)
#
#         output_data = dat[key]
#         if not output_data:
#             continue
#
#         if not overwrite and path.exists(output_path):
#             continue
#
#         with open(output_path, "wb") as output_file:
#             print("Writing '%s'..." % output_path)
#             output_file.write(output_data)


from os import path
from glob import glob

from formats.map.tdf import Terrain

extension = ".tdf"
validator_function = Terrain.read


base_paths = [r"C:\Work\ArkanumData",
              r"C:\Users\vleon1\AppData\Local\VirtualStore\Program Files (x86)\Arcanum",
              r"C:\Program Files (x86)\Arcanum"]


validated_objects = dict()


def validate_files(base_path):

    template = path.join(base_path, "*")

    for file_path in glob(template):

        if path.isdir(file_path):
            validate_files(file_path)

        elif file_path.lower().endswith(extension):
            print("Validating %s.." % file_path)
            validated_object = validator_function(file_path)
            validated_objects[file_path] = validated_object


for base_path in base_paths:
    validate_files(base_path)


print()
for validated_object_path, validated_object in validated_objects.items():

    print("Further Validating %s.." % validated_object_path)
    pass
