import argparse

from os import path
import os
from glob import glob

from typing import List

from formats.dat import Dat


class Constants(object):

    modules_folder = "modules"
    data_folder = "data"

    main_dat_names_template = "arcanum*.dat"
    module_dat_names_template = "*.dat"
    module_patch_dat_names_template = "*.patch*"

    arcanum_module_cased_name = "Arcanum"
    arcanum_module_lower_name = arcanum_module_cased_name.lower()


def get_dat_output_directory(dat_file_path: str, base_output_directory: str) -> str:

    dat_full_file_name = path.basename(dat_file_path)
    dat_base_file_name = path.splitext(dat_full_file_name)[0]

    dat_parent_directory = path.dirname(dat_file_path)
    dat_parent_folder = path.basename(dat_parent_directory)

    # If output path was specified. make sure that modules retain the modules parent directory..
    if base_output_directory and dat_parent_folder == Constants.modules_folder:
        base_output_directory = path.join(base_output_directory, Constants.modules_folder)

    # If no output path was specified then the parent folder should always be fine.
    if not base_output_directory:
        base_output_directory = dat_parent_directory

    if dat_parent_folder == Constants.modules_folder:

        # A hack that makes sure that in case of the arcanum module the code will work in a case sensitive
        # fashion to support cross platform extracting
        # I assume that if new modules will ever be created with 'PATCH' files, they will have the same case
        # name as the "dat" file.
        if dat_base_file_name.lower() == Constants.arcanum_module_lower_name:
            dat_output_folder = Constants.arcanum_module_cased_name
        else:
            dat_output_folder = dat_base_file_name

    else:
        dat_output_folder = Constants.data_folder

    return path.join(base_output_directory, dat_output_folder)


def extract_dat_file(dat_file_path: str, base_output_directory: str, list_only: bool, no_overwrite: bool) -> None:

    output_directory = get_dat_output_directory(dat_file_path=dat_file_path,
                                                base_output_directory=base_output_directory)

    dat = Dat.open(dat_file_path=dat_file_path)

    for key in dat.keys():

        if list_only:
            print("\t%s" % key)
            continue

        key_output_path = path.join(output_directory, key.replace('\\', os.sep))
        key_output_directory = path.dirname(key_output_path)

        if not path.exists(key_output_directory):
            os.makedirs(key_output_directory)

        output_data = dat[key]
        if not output_data:
            continue

        if no_overwrite and path.exists(key_output_path):
            continue

        print("\tExtracting '%s' to '%s'..." % (key, key_output_path))

        with open(key_output_path, "wb") as output_file:
            output_file.write(output_data)


def get_dat_paths(arcanum_directory: str) -> List[str]:

    main_dat_paths_template = path.join(arcanum_directory, Constants.main_dat_names_template)

    modules_directory = path.join(arcanum_directory, Constants.modules_folder)
    modules_main_dat_paths_template = path.join(modules_directory, Constants.module_dat_names_template)
    modules_patch_dat_paths_template = path.join(modules_directory, Constants.module_patch_dat_names_template)

    return (
        glob(main_dat_paths_template) + glob(modules_main_dat_paths_template) + glob(modules_patch_dat_paths_template)
    )


def main(input_path: str, output_directory: str, list_only: bool, no_overwrite: bool, delete_dat: bool) -> None:

    if path.isdir(input_path):
        dat_file_paths = get_dat_paths(input_path)
    else:
        dat_file_paths = [input_path]

    action = "Listing" if list_only else "Extracting"

    for dat_file_path in dat_file_paths:

        print("%s '%s'..." % (action, dat_file_path))

        extract_dat_file(dat_file_path=dat_file_path, base_output_directory=output_directory,
                         list_only=list_only, no_overwrite=no_overwrite)

        if delete_dat:
            os.remove(dat_file_path)
            print("Deleting '%s'..." % dat_file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Extracts the dat files of Arcanum.')
    parser.add_argument('input_path', help='Either the Arcanum directory or a dat file path, if the folder is used it '
                                           'will extract all the dat files of the game')
    parser.add_argument('--output_path', help='The base path for output files. '
                                              'note that this path is assumed to be an arcanum folder '
                                              'and thus will retain arcanum path conventions. '
                                              'In other words it will add "data" sub-folder for main dat files, '
                                              'and "modules/#module_name#" to module dat files.',
                        default='')
    parser.add_argument('--list-only', '-l', help='Specify to only list the content of the dat files',
                        action='store_true', default=False)
    parser.add_argument('--no-overwrite', help='Specify to skip overwriting destination files',
                        action='store_true', default=False)
    parser.add_argument('--delete-dat', help='Delete the dat file after extracting or listing',
                        action='store_true', default=False)

    arguments = parser.parse_args()

    main(input_path=arguments.input_path, output_directory=arguments.output_path,
         list_only=arguments.list_only, no_overwrite=arguments.no_overwrite, delete_dat=arguments.delete_dat)
