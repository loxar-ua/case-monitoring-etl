import gzip
from pathlib import Path

input_path = Path("https_www_pravda_com_ua_sitemap_sitemap-2025-12_xml.gz")
output_path = Path("unpacked_sitemap-2025-12.xml")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Визначаємо, чи файл дійсно gzip за першими байтами
with open(input_path, 'rb') as f_check:
    magic = f_check.read(2)
    is_gzip = magic == b'\x1f\x8b'

if is_gzip:
    with gzip.open(input_path, 'rt', encoding='utf-8') as f_in:
        content = f_in.read()
else:
    with open(input_path, 'r', encoding='utf-8') as f_in:
        content = f_in.read()

with open(output_path, 'w', encoding='utf-8') as f_out:
    f_out.write(content)

print(f"Файл розпаковано у: {output_path}")
