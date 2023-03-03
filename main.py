from pathlib import Path
from sys import argv
import shutil


FOLDERS = ('Images', 'Video', 'Documents', 'Audio', 'Archives', 'Unknown')
IMAGES = ('jpeg', 'png', 'jpg', 'svg')
VIDEO = ('avi', 'mp4', 'mov', 'mkv')
DOCS = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
AUDIO = ('mp3', 'ogg', 'wav', 'amr')
ARCHIVES = ('zip', 'gz', 'tar')


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = (
    'a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
    'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu', 'ya', 'je', 'i', 'ji', 'g'
)
PROBLEM_SYMBOLS = ' !"#$%^&*()-+№;:?,>=<~\'{[]}|\\/@'
TRANS = {}

for cyrillic, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = translation
    TRANS[ord(cyrillic.upper())] = translation.upper()


def normalize(name: str) -> str:
    for char in PROBLEM_SYMBOLS:
        name = name.replace(char, '_')
    return name.translate(TRANS)


directory = Path(argv[1])


def create_folders():  # Создаем папки для последующих перемещений
    for folder_name in FOLDERS:
        try:
            new_folder = Path(f'{argv[1]}/{folder_name}')
            # можно передать exist_ok=True и не обрабатывать исключение, но так красивее :D
            new_folder.mkdir()
        except FileExistsError:
            print(f'Папка с именем {folder_name} уже существует')


def replace_files():
    for extension in IMAGES:
        for file in directory.glob(f'**/*.{extension}'):
            new_path = directory / FOLDERS[0] / normalize(file.name)
            file.rename(new_path)

    for extension in VIDEO:
        for file in directory.glob(f'**/*.{extension}'):
            new_path = directory / FOLDERS[1] / normalize(file.name)
            file.rename(new_path)

    for extension in DOCS:
        for file in directory.glob(f'**/*.{extension}'):
            new_path = directory / FOLDERS[2] / normalize(file.name)
            file.rename(new_path)

    for extension in AUDIO:
        for file in directory.glob(f'**/*.{extension}'):
            new_path = directory / FOLDERS[3] / normalize(file.name)
            file.rename(new_path)

    for extension in ARCHIVES:
        for file in directory.glob(f'**/*.{extension}'):
            new_path = directory / FOLDERS[4] / normalize(file.name)
            file.rename(new_path)


def unpuck_archive():
    archive_directory = Path(f'{argv[1]}/{FOLDERS[4]}')
    for archive in archive_directory.glob('**/*'):
        path_archive_folder = f'{argv[1]}/{FOLDERS[4]}/{archive.name}'
        archive_name = archive.name
        shutil.unpack_archive(archive_name, path_archive_folder)


def delete_empty_folders():
    empty_folders = []
    for folder in directory.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            empty_folders.append(folder)

    for folder in empty_folders:
        shutil.rmtree(str(folder))
        print(f'Папка {folder} была удалена')


if __name__ == '__main__':
    create_folders()
    replace_files()
    unpuck_archive()
    delete_empty_folders()
