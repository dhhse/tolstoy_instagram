import re
import pandas as pd

from cgi import escape
from lxml import etree
from tqdm import tqdm


def assemble_title_stmt(row_dict):
    """Добавляет раздел с данными об авторе фотографии и её текущем владельце.

    :param row_dict: (dict) описание фотографии
    :return: titleStmt: (str) описание в TEI
    """
    if row_dict["AUTHOR"] != "-1":
        author = "<author>{}</author>".format(escape(row_dict["AUTHOR"]))
    else:
        author = ""
    funder = "<funder>Государственный музей Л.Н. Толстого</funder>"
    titleStmt = "<titleStmt>{}{}</titleStmt>".format(author, funder)
    return titleStmt


def assemble_publication_stmt(row_dict):
    """Добавляет раздел с данными об ИД фотографии, коллекциях, рубриках и том,
    как она попала в музей.

    :param row_dict: (dict) описание фотографии
    :return: publicationStmt: (str) описание в TEI
    """
    acquisition = "<acquisition>{}</acquisition>".format(row_dict["IWAY"]) \
                if row_dict["IWAY"] != "-1" else ""
    nfond = "<collection type=\"nfond\">{}</collection>".format(row_dict["NFOND"]) \
            if row_dict["NFOND"] != "-1" else ""
    spiex = "<collection type=\"spiex\">{}</collection>".format(row_dict["SPIEX"]) \
            if row_dict["SPIEX"] != "-1" else ""
    identif = "<idno type=\"identif\">{}</idno>".format(row_dict["IDENTIF"]) \
            if row_dict["IDENTIF"] != "-1" else ""
    inv = "<idno type=\"inv\">{}</idno>".format(row_dict["INV"]) \
        if row_dict["INV"] != "-1" else ""
    category = "<category>{}</category>".format(row_dict["SPIRUBR"]) \
            if row_dict["SPIRUBR"] != "-1" else ""
    publisher = "<publisher>{}</publisher>".format(row_dict["VLAD"]) \
            if row_dict["VLAD"] != "-1" else ""
    publicationStmt = "<publicationStmt>{}{}{}{}{}{}{}</publicationStmt>".format(acquisition,
                        nfond, spiex, identif, inv, category, publisher)
    return publicationStmt


def extract_creat(row_dict):
    """Извлекает информацию о дате создания.
        CREAT = известна точная дата
        CREAT1 = известна дата "не ранее"
        CREAT2 = известна дата "не позднее"

    :param row_dict: (dict) описание фотографии
    :return: dateCreat: (str) TEI-элемент
    """
    if row_dict["CREAT"] == "-1":
        dateCreat = ""
        if row_dict["CREAT1"] != "-1":
            dateCreat += "<date type=\"created notBefore\">{}</date>".format(escape(str(row_dict["CREAT1"])))
        if row_dict["CREAT2"] != "-1":
            dateCreat += "<date type=\"created notAfter\">{}</date>".format(escape(str(row_dict["CREAT2"])))
    else:
        dateCreat = "<date type=\"created\">{}</date>".format(escape(row_dict["CREAT"]))
    return dateCreat


def extract_sizes(sizes_str, reg_sizes):
    """Извлекает информацию о физических размерах снимка с помощью регулярного выражения.

    :param sizes_str: (str) запись музейных хранителей
    :param reg_sizes: (regex) регулярное выражение для обработки записей
    :return: width: (str) строка-ширина
    :return: height: (str) строка-высота
    """
    extraction = re.search(reg_sizes, sizes_str)
    width = extraction.group(1)
    height = extraction.group(2)
    return width, height


def assemble_source_desc(row_dict, reg_sizes):
    """Добавляет раздел с физическим описанием фотографии.

    :param row_dict: (dict) описание фотографии
    :param reg_sizes: (regex) регулярное выражение для обработки записей
    музейных хранителей о размерах фотографии

    :return: sourceDesc: (str) описание в TEI
    """
    origPlace = "<origPlace>{}</origPlace>".format(row_dict["GEOGR"]) \
        if row_dict["GEOGR"] != "-1" else ""
    dateCreat = extract_creat(row_dict)
    distributor = "<distributor>{}</distributor>".format(escape(row_dict["IZGOT"])) \
        if row_dict["IZGOT"] != "-1" else ""
    source = "<source>{}</source>".format(row_dict["NCOMP"]) \
        if row_dict["NCOMP"] != "-1" else ""
    if row_dict["SIZES"] != "-1":
        try:
            width, height = extract_sizes(row_dict["SIZES"], reg_sizes)
            dimensions = "<dimensions><width>{} см</width><height>{} см</height></dimensions>".format(width, height)
        except:
            dimensions = ""
    else:
        dimensions = ""
    desc = "<desc>{}</desc>".format(escape(str(row_dict["COMPNAM"]))) \
        if row_dict["COMPNAM"] != "-1" else ""
    metamark = "<metamark>{}</metamark>".format(row_dict["INSCR"]) \
        if row_dict["INSCR"] != "-1" else ""
    sourceDesc = "<sourceDesc>{}{}{}{}{}{}{}</sourceDesc>".format(origPlace,
                dateCreat, distributor, source, dimensions, desc, metamark)
    return sourceDesc


def assemble_revision_desc(row_dict):
    """Добавляет раздел изменений.

    :param row_dict: (dict) описание фотографии
    :return: revisionDesc: (str) описание в TEI
    """
    revisionDesc = "<revisionDesc><change when=\"2020-04-15\">конвертация в TEI из КАМИС</change></revisionDesc>"
    return revisionDesc


def load_data():
    """Загружает таблицу с метаданными.

    :return: df: (pd.DataFrame) - метаданные
    """
    df = pd.read_csv("./data/metadata_kamisHeader.tsv", sep="\t", encoding="utf-8")
    df["id"] = df["id"].astype("str").apply(lambda x: "0" * (8 - len(x)) + x)
    return df


def build_tei(row_dict, reg_sizes):
    """Собирает TEI-описание.

    :param row_dict: (dict) словарь-описание фотографии
    :param reg_sizes: (regex) регулярка для работы с размерами фотографии
    :return: overallTEI: (str) описание одной строкой
    """
    title = assemble_title_stmt(row_dict)
    source = assemble_source_desc(row_dict, reg_sizes)
    publication = assemble_publication_stmt(row_dict)
    fileDesc = "<fileDesc>{}{}{}</fileDesc>".format(title, publication, source)
    revisionDesc = assemble_revision_desc(row_dict)
    overallTEI = "<TEI xmlns=\"http://www.tei-c.org/ns/1.0\" xml:lang=\"rus\"><teiHeader>{}{}</teiHeader></TEI>".format(
        fileDesc, revisionDesc)
    return overallTEI


def save_TEI(tei_desc, photo_id):
    """Сохраняет результат. Если при проверке на валидность произошла ошибка,
    вместо записи в файл выводит в stdout.

    :param tei_desc: (str) описание
    :param photo_id: (str) ИД фотографии для названия файла
    :return: None
    """
    try:
        root = etree.fromstring(tei_desc)
        tree = root.getroottree()
        tree.write("./data/tei/{}.xml".format(photo_id), xml_declaration=True,
                   pretty_print=True, encoding="utf-8")
    except:
        print(photo_id)
        print(tei_desc)
        print("===")


def main():
    reg_sizes = re.compile("([0-9]{1,2}(?:[,\.][0-9])?) ?х ?([0-9]{1,2}(?:[,\.][0-9])?)")
    df = load_data()

    for row in tqdm(range(len(df))):
        row_dict = df.iloc[row].to_dict()
        photo_id = row_dict["id"]
        overall_TEI = build_tei(row_dict, reg_sizes)
        save_TEI(overall_TEI, photo_id)


if __name__ == "__main__":
    main()
