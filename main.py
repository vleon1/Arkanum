from os import path
import os
from glob import glob
from itertools import groupby

from formats.map.tdf import Terrain, Descriptor
from formats.map.prp import MapProperties

from typing import List

extension = ".tdf"
validator_function = Terrain.read


base_paths = glob(r"D:\Games\Arcanum\modules\Arcanum\maps\Arcanum1-024-fixed")  # glob(r"D:\Games\Arcanum")


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

    all_types = set(Descriptor.Type.all)
    combined_types = set(Descriptor.Type.combined)
    assert len(Descriptor.Type.all) == 20
    assert len(Descriptor.Type.all) == len(list(all_types))

    print(flush=True)
    for validated_object in validated_objects:

        print("Validating descriptors of %s.." % validated_object.file_path, flush=True)
        if not validated_object.has_descriptors:
            continue
        for col in range(validated_object.cols):
            for row in range(validated_object.rows):

                descriptor = validated_object[row, col]

                assert 0 <= descriptor.index <= 11

                if descriptor.index > 3:
                    assert descriptor.terrain_type in combined_types
                else:
                    assert descriptor.terrain_type in all_types


if __name__ == "__main__":
    main()
