import os
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


def main():
    kamis_tags = ["ATRIB", "AUTHOR", "AUTHORF", "AUTHORR", "COLPR", "COMM", "COMPNAM", "CONNEC", "CREAT", "CREAT1",
    "CREAT2", "DEFPNAM", "DESCM", "DESCRI", "ENDAT", "ENDAT1", "ENDAT2", "GEOGR", "IDENTIF", "INSCR", "INV", "IWAY",
    "IZGOT", "LEGENDA", "NCOMP", "NDEFWD", "NFOND", "NOMGC", "PNAM", "PROISX", "SIZES", "SODERG", "SPIEX", "SPILIT",
    "SPIPERS", "SPIRUBR", "VLAD"]
    info = {t: [] for t in kamis_tags}
    info["path_xml"] = []
    info["path_miniature"] = []
    info["path_fullsize"] = []
    info["id"] = []
    xml_folder = "./xmls"
    xmls = [x for x in os.listdir(xml_folder) if x.endswith(".xml")]
    for item in tqdm(xmls):
        path_to_xml = os.path.join(xml_folder, item)
        path_mini = path_to_xml.replace("xmls", "miniatures")
        path_full = path_to_xml.replace("xmls", "fullsize")
        with open(path_to_xml, "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "lxml")
        info["id"].append(item[:-4])
        info["path_xml"].append(path_to_xml)
        info["path_miniature"].append(path_mini)
        info["path_fullsize"].append(path_full)
        for kamis_t in kamis_tags:
            try:
                value = soup.find(kamis_t.lower()).get_text(strip=True)
            except:
                value = -1
            info[kamis_t].append(value)
    df_total = pd.DataFrame.from_dict(info)
    df_total = df_total.set_index("id")
    df_total.to_csv("./metadata.csv", sep=";")


if __name__ == "__main__":
    main()