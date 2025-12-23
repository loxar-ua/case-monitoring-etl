import json
from math import ceil

from src.database.service import form_clusters


def run_forming_clusters():
    clusters_info = []
    with open('data/clusters_info.jsonl', 'r') as json_file:
        for line in json_file:
            clusters_info.append(json.loads(line))

    clusters_info = clusters_info[-53:]
    n = len(clusters_info)
    chunk_size = 1
    chunk_number =  ceil(n / chunk_size)

    for i in range(chunk_number):
        chunk_start = i * chunk_size
        chunk_end = min((i + 1) * chunk_size, n)
        form_clusters(clusters_info[chunk_start:chunk_end])


if __name__ == '__main__':
    run_forming_clusters()