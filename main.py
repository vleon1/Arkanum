from os import path
import os
from glob import glob

from formats.map.tdf import Terrain, Descriptor, terrain_types
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

    print(flush=True)
    for validated_object in validated_objects:

        print("Validating descriptors of %s.." % validated_object.file_path, flush=True)
        if not validated_object.has_descriptors:
            continue

        for col in range(validated_object.cols):
            for row in range(validated_object.rows):

                descriptor = validated_object[row, col]

                # complex_indexes = {4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56}
                #
                # assert 0 <= descriptor.from_terrain_index < len(terrain_types)
                # assert 0 <= descriptor.to_terrain_index < len(terrain_types)
                #
                # if descriptor.from_terrain_index == descriptor.to_terrain_index:
                #     assert 0 <= descriptor.index <= 3
                # else:
                #     assert descriptor.index in complex_indexes

                if descriptor.from_terrain_index == 5 and descriptor.to_terrain_index == 2:
                    tile_row = 64 * row + 32
                    tile_col = 64 * col + 32
                    data = "'%s to %s' at (%d, %d) with index (%d) full descriptor (0x%04X)" % \
                           (descriptor.from_terrain, descriptor.to_terrain, tile_row, tile_col, descriptor.index,
                            descriptor.index_and_terrain_type)
                    print(data, flush=True)

if __name__ == "__main__":
    main()
