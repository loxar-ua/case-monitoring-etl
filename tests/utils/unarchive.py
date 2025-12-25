import requests
import gzip
import shutil
from pathlib import Path

def download_and_unpack_gz(url: str, filename: str):
    """
    Downloads a .xml.gz file from a URL, decompresses it, and writes it to a file.

    :param url: URL to the .xml.gz file
    :param output_file: path to the file where the decompressed XML will be saved
    """
    output_dir = Path("/Users/llesya/case-monitoring-etl/tests/fixtures/liga")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with gzip.GzipFile(fileobj=response.raw) as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

download_and_unpack_gz(
    "https://www.radiosvoboda.org/sitemap_9_news.xml.gz",
    "part1.xml"
)
