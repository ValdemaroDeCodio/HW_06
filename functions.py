from constants import *
from pathlib import Path
import shutil


def normalize(name: str) -> str:
    return name.translate(TRANS)


def create_folders(directory):
    for folder_name in CATEGORIES.keys():
        try:
            new_folder = directory / folder_name
            new_folder.mkdir()
        except FileExistsError:
            print(f'Folder named {folder_name} already exists.')


def find_replace(directory: Path, file: Path):
    for category, extensions in CATEGORIES.items():
        new_path = directory / category
        if not extensions:
            file.replace(new_path / normalize(file.name))
            return None
        if file.suffix.lower() in extensions:
            file.replace(new_path / normalize(file.name))
            return None

    return None


def replace_files(directory: Path):
    for file in directory.glob(f'**/*.*'):
        find_replace(directory, file)


def unpack_archive(directory: Path):
    archive_directory = directory / 'ARCHIVES'
    for archive in archive_directory.glob('*.*'):
        path_archive_folder = archive_directory / archive.stem.upper()
        shutil.unpack_archive(archive, path_archive_folder)


def delete_empty_folders(directory: Path):
    empty_folders = []
    for folder in directory.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            empty_folders.append(folder)

    for folder in empty_folders:
        shutil.rmtree(str(folder))
        print(f'{folder} folder deleted.')
