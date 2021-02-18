import os
import re
import zipfile

from shutil import Error as shError
from shutil import move
from shutil import rmtree


def set_starting_params():
    """Ввод путей к папкам и их предварительная обработка с защитой юзера от
    самого себя.

    :arg None

    :return: archive_path: (str) путь к архиву
    :return: extraction_folder: (str) папка для распаковки
    """
    archive_path = input("Введите путь к архиву: ")

    extraction_folder = input("Введите путь к папке для распаковки: ")

    correct_params = False
    while not correct_params:
        clear = bool(input("Очистить папку для распаковки перед началом работы? (True/False): "))
        if clear and extraction_folder != ".":
            correct_params = True
            rmtree(extraction_folder)
        else:
            print("Невозможно очистить текущую папку, выберите другую папку")
    return archive_path, extraction_folder


def create_dirs(extraction_folder, folders):
    """Создаёт папки, которых не хватает.

    :param extraction_folder: (str) путь к папке для распаковки от юзера
    :param folders: (dict) папки для основного хранения
    :return: None
    """
    for folder in [extraction_folder, "./data"] + list(folders.values()):
        if not os.path.exists(folder):
            os.mkdir(folder)


def decide_on_type(file_name):
    """По названию файла определяет его тип (XML-описание, миниатюра или
    полноразмерная фотография).

    :param file_name: (str) имя файла
    :return: file_type: (str) тип файла
    """
    file_type = ""
    if file_name.endswith(".jpg"):
        if "image1" in file_name:
            file_type = "mini"
        elif "image2" in file_name:
            file_type = "full"
    elif file_name.endswith(".xml"):
        if file_name != "content.xml":
            file_type = "desc"
    return file_type


def move_file(file_path, file_type, folders):
    """Копирует файл в нужную папку в зависимости от его типа.

    :param file_path: (str) путь к файлу
    :param file_type: (str) тип
    :param folders: (dict) папки для основного хранения
    :return: None
    """
    new_folder = folders[file_type]
    move(file_path, new_folder)


def remove_prefixes(folder):
    """Для папок, в которых лежат картинки, обрезать префиксы image1/image2,
    отвечающие за размер.

    :param folder: (str) папка
    :return: None
    """
    reg_photo_prefix = re.compile("image[12]_")
    for photo_name in os.listdir(folder):
        if photo_name != ".DS_Store":
            old_name = os.path.join(folder, photo_name)
            new_name = os.path.join(folder, reg_photo_prefix.sub("", photo_name))
            os.rename(old_name, new_name)


def unzip_archive(archive_path, extraction_folder, folders):
    """Распаковывает архив с выгрузкой из КАМИСа в нужную папку, уплощает структуру
    и распределяет содержимое по папкам.

    :param archive_path: (str) путь к архиву
    :param extraction_folder: (str) путь к папке, в которую распаковываем
    :param folders: (dict) папки для основного хранения
    :return: None
    """
    with zipfile.ZipFile(archive_path, "r") as photos_zip:
        photos_zip.extractall(extraction_folder)
    # архивы внутри архивов
    for archive_file in os.listdir(extraction_folder):
        small_archive_path = os.path.join(extraction_folder, archive_file)
        with zipfile.ZipFile(small_archive_path, "r") as data_zip:
            data_zip.extractall(extraction_folder)
        os.remove(small_archive_path)


def replace_files(extraction_folder, folders):
    """Перемещает файлы по их типам.

    :param extraction_folder: (str) путь к папке, в которую распаковываем
    :param folders: (dict) папки для основного хранения
    :return: None
    """
    for root, dirs, files in os.walk(extraction_folder):
        for file in files:
            file_old = os.path.join(root, file)
            file_new = os.path.join(root, file.replace("\\", "_"))
            os.rename(file_old, file_new)
            file_type = decide_on_type(file)
            if file_type != "":
                try:
                    move_file(file_new, file_type, folders)
                except shError as e:
                    print(file_new, e)



def check_presence(path_to_kamis):
    """Проверяет, есть ли фотографии для описаний КАМИС. Недостающие записывает
    в файл.

    :param path_to_kamis: (str) путь к папке с описаниями
    :return: None
    """
    items = sorted([file[:-4] for file in os.listdir(path_to_kamis)
                    if file.endswith(".xml")])
    lack = {}
    for item in items:
        if not os.path.exists(os.path.join(f"./data/fullsize/{item}.jpg")):
            lack[item] = ["full"]
        if not os.path.exists(os.path.join(f"./data/miniatures/{item}.jpg")):
            lack[item].append("mini")
    print("Не хватает фотографий у {} описаний".format(len(lack)))
    if os.path.exists("./lack.txt"):
        f = open("./lack.txt", "r", encoding="utf-8")
    else:
        f = open("./lack.txt", "w", encoding="utf-8")
    for item in sorted(lack.keys()):
        lacking = ", ".join(lack[item])
        f.write(f"{item}: {lacking}\n")
    f.close()


def main():
    # подготовка
    archive_path, extraction_folder = set_starting_params()
    folders = {
        "mini": "./data/miniatures",
        "full": "./data/fullsize",
        "desc": "./data/kamis"
    }
    create_dirs(extraction_folder, folders)
    # распаковка и перемещение
    unzip_archive(archive_path, extraction_folder, folders)
    replace_files(extraction_folder, folders)
    # уборка
    remove_prefixes("./data/fullsize")
    remove_prefixes("./data/miniatures")
    # проверка
    # check_presence("./data/kamis")


if __name__ == "__main__":
    main()
