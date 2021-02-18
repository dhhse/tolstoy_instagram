import pandas as pd
import os

from bs4 import BeautifulSoup
from tqdm import tqdm


def parse_photo_desc(item, info, kamis_tags):
    """Обрабатывает XML-файл с описанием фотографии, использующим тагсет КАМИС.

    :param item: (str) описание фотографии
    :param info: (dict) общий словарь со сведениями по всем фотографиям
    :param kamis_tags: (list) тагсет/ключи словаря info

    :return: info: (dict) словарь с новыми данными
    """
    path_to_desc = os.path.join("./data/kamis", item)
    with open(path_to_desc, "r", encoding="utf-8") as f:
        content = f.read()
        soup = BeautifulSoup(content, "lxml")
    info["id"].append(item[:-4])
    for kamis_tag in kamis_tags:
        try:
            value = soup.find(kamis_tag.lower()).get_text(strip=True).replace("\n", "")
        except:
            value = -1
        info[kamis_tag].append(value)
    return info


def save_as_csv(info):
    """Сохраняет метаданные. Если файл с метаданными уже есть, дописывает новые,
    сортирует и сохраняет результат.

    :param info: (dict) общий словарь со сведениями по всем фотографиям
    :return None
    """
    df_total = pd.DataFrame.from_dict(info)
    df_total = df_total.set_index("id")
    path_tsv = "./data/metadata.tsv"
    if os.path.exists(path_tsv):
        df_prev = pd.read_csv(path_tsv, sep="\t", encoding="utf-8")
        df_prev = df_prev.set_index("id")
        df_total = df_prev.append(df_total).sort_index()
    df_total.to_csv(path_tsv, sep="\t")


def main():
    kamis_tags = ["AUTHOR", "COMPNAM", "CREAT", "CREAT1", "CREAT2", "DESCRI",
                  "GEOGR", "IDENTIF", "INSCR", "INV", "IWAY", "IZGOT", "NCOMP",
                  "NFOND", "PNAM", "SIZES", "SPIEX", "SPIRUBR", "VLAD"]
    info = {t: [] for t in kamis_tags}
    info["id"] = []
    files_to_parse = [x for x in os.listdir("./data/kamis")
                      if x.endswith(".xml")]
    for file in tqdm(files_to_parse):
        info = parse_photo_desc(file, info, kamis_tags)
    save_as_csv(info)


if __name__ == "__main__":
    main()
