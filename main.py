from os import path
from glob import glob

from formats.map.tdf import Terrain

from typing import List

extension = ".tdf"
validator_function = Terrain.read


base_paths = glob(r"D:\Games\Arcanum")


def validate_files(directory: str, validated_objects: List[Terrain]):

    template = path.join(directory, "*")

    for file_path in glob(template):

        if path.isdir(file_path):
            validate_files(file_path, validated_objects)

        elif file_path.lower().endswith(extension):
            print("Validating %s.." % file_path)
            validated_object = validator_function(file_path)
            validated_objects.append(validated_object)


def main():

    validated_objects = []  # type: List[Terrain]

    for base_path in base_paths:
        validate_files(base_path, validated_objects)

    print(flush=True)
    for validated_object in validated_objects:

        print("Further validation of %s.." % validated_object.file_path, flush=True)


if __name__ == "__main__":
    main()
