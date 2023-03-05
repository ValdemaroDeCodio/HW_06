from constants import *
from functions import *
from sys import argv


def print_in_cmd(directory):
    for folder in directory.glob('*'):
        files_name = [file.name for file in folder.iterdir() if file.is_file()]
        files_ext = set(file.suffix for file in folder.iterdir()
                        if file.is_file())

        print(f'Files names in {folder.name}: \n{files_name}')
        print(f'Files extensions in {folder.name}: \n{files_ext}')
        print('_' * 30)


if __name__ == '__main__':
    try:
        directory = Path(argv[1])
    except IndexError:
        print("Must be path to folder")

    if not directory.exists():
        print("The folder doesn't exist")
    else:
        create_folders(directory)
        replace_files(directory)
        unpack_archive(directory)
        delete_empty_folders(directory)
        print_in_cmd(directory)
