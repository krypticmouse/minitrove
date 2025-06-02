import csv
import fsspec

from typing import Dict


COMPRESSION_TYPES = {
    "gz": "gzip",
    "gzip": "gzip",
    "bz2": "bz2",
    "bzip2": "bz2",
    "xz": "lzma",
    "lzma": "lzma",
    "zip": "zip",
}


def get_compression(path: str):
    compression_extension = path.split(".")[-1]
    assert compression_extension in COMPRESSION_TYPES, f"Compression extension `{compression_extension}` not supported. Supported extensions are {list(COMPRESSION_TYPES.keys())}"

    return COMPRESSION_TYPES[compression_extension]


def fetch_csv_schema(path: str, sep: str = ",") -> Dict[str, int]:
    with fsspec.open(path) as f:
        reader = csv.reader(f, delimiter=sep)
        header = next(reader)
        return {col: i for i, col in enumerate(header)}