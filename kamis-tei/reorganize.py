import os
from shutil import copy2


def decide_on_type(file_name):
    file_type = "yo"
    if file_name.endswith(".jpg"):
        if file_name.startswith("image1"):
            file_type = "mini"
        elif file_name.startswith("image2"):
            file_type = "full"
    elif file_name.endswith(".xml"):
        if file_name != "content.xml":
            file_type = "desc"
    return file_type


def copy_file(file_path, file_type):
    folder_miniature = "./data_raw/miniatures"
    folder_full = "./data_raw/fullsize"
    folder_desc = "./data_raw/xmls"
    if file_type == "mini":
        copy2(file_path, folder_miniature)
    elif file_type == "full":
        copy2(file_path, folder_full)
    elif file_type == "desc":
        copy2(file_path, folder_desc)


def main():
    # src_folders = [f for f in os.listdir("./data_raw/") if f.startswith("0")]
    # for src_folder in src_folders:
    #     mini_folders = [f for f in os.listdir(f"./data_raw/{src_folder}") if f != ".DS_Store"]
    #     for mini_folder in mini_folders:
    #         folder_path = f"./data_raw/{src_folder}/{mini_folder}" 
    #         for item in os.listdir(folder_path):
    #             src_file_path = folder_path + "/" + item
    #             file_type = decide_on_type(item)
    #             copy_file(src_file_path, file_type)
    folder_miniature = "./data_raw/miniatures"
    minis = len([f for f in os.listdir(folder_miniature) if f.endswith(".jpg")])
    folder_full = "./data_raw/fullsize"
    fulls = len([f for f in os.listdir(folder_full) if f.endswith(".jpg")])
    folder_desc = "./data_raw/xmls"
    descs = len([f for f in os.listdir(folder_desc) if f.endswith(".xml")])
    print("miniature", minis)
    print("fulls", fulls)
    print("descs", descs)



if __name__ == "__main__":
    main()
