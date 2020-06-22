# Инстаграм Л.Н. Толстого
Ресурсы и код проекта «Инстаграм Толстого» (DH-магистры Вышки, Государственный музей Л.Н. Толстого)

## Что тут есть?

### Датасеты
Датасет по фотографиям, основанный на тегах КАМИС (сырая версия): [.csv (2.03 MB)](./datasets/tolstoy_photos.csv). Там же лежит версия, в которой остались только те столбцы, в которых были данные: [без лишних столбцов](./datasets/tolstoy_photos_no_empty_columns.csv)

_Подчищенный датасет в процессе подготовки!_

### Работа с данными

**Распаковка архива и организация файлов:** [скрипт](./unzip_and_reorganize.py).

**Сбор датасета из КАМИС-описаний:** [скрипт](./kamis_to_csv.py).

**Конвертация КАМИС-TEI:** 

- [соответствие тегов](./kamis-tei/kamis_tags_to_TEI.tsv), 

- [модель TEI-описания](./kamis-tei/TEI_desc_for_photos_sample.xml), 

- [код конвертера](./kamis-tei/kamis_to_tei.py).

База данных из метаданных фотографий: см. [репозиторий с исходным кодом сайта](https://github.com/creaciond/tolstoy_photodb_site).

## Выступления
14 апреля 2020 — [Digital History Meetup]() в Минске (спасибо, Аня!). Новость на сайте Вышки [тут](https://hum.hse.ru/digital/news/354335283.html). Слайды [тут](https://creaciond.github.io/slides/conferences/202003_digital_history_meetup_minsk.pdf).
