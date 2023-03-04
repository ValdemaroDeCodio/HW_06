from pathlib import Path
from sys import argv
import shutil

# FOLDERS = ('Images', 'Video', 'Documents', 'Audio', 'Archives', 'Unknown'),

CATEGORIES = dict(IMAGES = ('.jpeg', '.png', '.jpg', '.svg'),
                VIDEO = ('.avi', '.mp4', '.mov', '.mkv'),
                DOCS = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
                AUDIO = ('.mp3', '.ogg', '.wav', '.amr'),
                ARCHIVES = ('.zip', '.gz', '.tar'),
                OTHER = None
                )


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

for symbol in PROBLEM_SYMBOLS:
    TRANS[ord(symbol)] = "_"



def normalize(name: str) -> str:
    # for char in PROBLEM_SYMBOLS:
    #     name = name.replace(char, '_')
    return name.translate(TRANS)


def create_folders(directory):  # Создаем папки для последующих перемещений
    for folder_name in CATEGORIES.keys():
        try:
            new_folder = directory / folder_name #Path(f'{argv[1]}/{folder_name}')
            # можно передать exist_ok=True и не обрабатывать исключение, но так красивее :D
            new_folder.mkdir()
        except FileExistsError:
            print(f'Папка с именем {folder_name} уже существует')


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
        
    # find_replace(IMAGES, 0)

    # find_replace(VIDEO, 1)

    # find_replace(DOCS, 2)

    # find_replace(AUDIO, 3)

    # find_replace(ARCHIVES, 4)


def unpack_archive(directory: Path):
    archive_directory = directory / 'ARCHIVES' #Path(f'{argv[1]}/{FOLDERS[4]}')
    for archive in archive_directory.glob('*.*'):
        path_archive_folder = archive_directory / archive.stem.upper()
        # archive_name = archive.name
        shutil.unpack_archive(archive, path_archive_folder)


def delete_empty_folders(directory:Path):
    empty_folders = []
    for folder in directory.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            empty_folders.append(folder)

    for folder in empty_folders:
        shutil.rmtree(str(folder))
        print(f'Папка {folder} была удалена')


if __name__ == '__main__':
    try:
        directory = Path(argv[1])
    except IndexError:
        print("Must be path to folder")
    
    if not directory.exists():
        print("The folder dos't exist")
    else:
        create_folders(directory)
        replace_files(directory)
        unpack_archive(directory)
        delete_empty_folders(directory)
    # print(normalize('Ки№ї,%в'))
