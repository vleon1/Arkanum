from os import path
from glob import glob
from collections import OrderedDict

from formats.map.tdf import Terrain
from formats.map.prp import MapProperties

from typing import Dict

extension = ".prp"
validator_function = MapProperties.read


base_path = r"D:\Games\Arcanum"


def validate_files(directory, validated_objects):

    template = path.join(directory, "*")

    for file_path in glob(template):

        if path.isdir(file_path):
            validate_files(file_path, validated_objects)

        elif file_path.lower().endswith(extension):
            print("Validating %s.." % file_path)
            validated_object = validator_function(file_path)
            validated_objects[file_path] = validated_object


def main():

    validated_objects = OrderedDict()  # type: Dict[str, MapProperties]

    validate_files(base_path, validated_objects)

    print()
    for validated_object_path, validated_object in validated_objects.items():
        print("Further Validating %s.." % validated_object_path)

        assert path.basename(validated_object_path).lower() == "map.prp"

        validated_object_directory = path.dirname(validated_object_path)
        terrain_path = path.join(validated_object_directory, "terrain.tdf")

        Terrain.read(terrain_path)

    pass


if __name__ == "__main__":
    main()
