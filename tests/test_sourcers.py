import os
import pytest

from tqdm import tqdm


@pytest.fixture
def uncompressed_data():
    return {
        "csv": "tests/fixtures/sources/standard/data.csv",
        "txt": "tests/fixtures/sources/standard/sample.txt",
        "json": "tests/fixtures/sources/standard/data.jsonl",
    }


@pytest.fixture
def compressed_data():
    return {
        "csv_bz2": "tests/fixtures/sources/compressed/data.csv.bz2",
        "json_xz": "tests/fixtures/sources/compressed/data.jsonl.xz",
        "txt_gz": "tests/fixtures/sources/compressed/sample.txt.gz",
    }
