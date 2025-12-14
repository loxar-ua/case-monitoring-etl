import requests
import gzip
import shutil
from pathlib import Path

def download_and_unpack_gz(url: str, filename: str):
    """
    Завантажує .xml.gz за URL, розпаковує та записує у файл.

    :param url: URL до .xml.gz
    :param output_file: шлях до файлу, куди зберегти розпакований XML
    """
    output_dir = Path("/Users/llesya/case-monitoring-etl/tests/fixtures/svoboda")
    output_dir.mkdir(parents=True, exist_ok=True)  # створюємо директорію, якщо немає

    output_path = output_dir / filename

    # Завантажуємо файл
    response = requests.get(url, stream=True)
    response.raise_for_status()  # кинути помилку, якщо не 200

    # Розпаковуємо gzip на льоту та записуємо у файл
    with gzip.GzipFile(fileobj=response.raw) as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"Файл з {url} розпаковано у {output_path}")

download_and_unpack_gz(
    "https://zn.ua/pub/sitemaps/part7.xml.gz",
    "part1.xml"
)
