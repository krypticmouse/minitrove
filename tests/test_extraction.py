import os
import pytest

from tqdm import tqdm
from fastdiff import compare

from databrix.extract.extractors import ResiliparseExtractor, TrafilaturaExtractor
from databrix.schema.extract import ResiliparseConfig, TrafilaturaConfig


INPUT_PATH = "tests/fixtures/extract/html"
EXPECTED_PATH = "tests/fixtures/extract/expected"
OUTPUT_PATH = "tests/fixtures/extract/output"
DIFF_PATH = "tests/fixtures/extract/diff"


@pytest.fixture
def html_data():
    return [
        (file, open(os.path.join(INPUT_PATH, file), "r").read())
        for file in os.listdir(INPUT_PATH)
    ]


def test_resiliparse_extractor(html_data):
    extractor = ResiliparseExtractor(
        ResiliparseConfig(
            preserve_formatting=True,
            main_content=True,
        )
    )
    results = extractor.extract([data for _, data in html_data])

    os.makedirs(os.path.join(OUTPUT_PATH, "resiliparse"), exist_ok=True)
    os.makedirs(os.path.join(DIFF_PATH, "resiliparse"), exist_ok=True)

    for idx, result in tqdm(enumerate(results), desc="Writing results"):
        with open(os.path.join(OUTPUT_PATH, "resiliparse", html_data[idx][0].replace(".html", ".txt")), "w") as f:
            print(result, file=f)

        with open(os.path.join(EXPECTED_PATH, "resiliparse", html_data[idx][0].replace(".html", ".txt")), "r") as expected_f, \
            open(os.path.join(DIFF_PATH, "resiliparse", html_data[idx][0].replace(".html", ".diff")), "w") as diff_f:
            expected = expected_f.read().rstrip('\n')
            
            if result != expected:
                diffs = compare(result, expected)
                print(diffs, file=diff_f)
            else:
                print("No differences found.", file=diff_f)
            
            assert result == expected, f"Failed on {html_data[idx][0]}"


def test_trafilatura_extractor(html_data):
    extractor = TrafilaturaExtractor(
        TrafilaturaConfig(
            favor_recall=True,
        )
    )
    results = extractor.extract([data for _, data in html_data])

    os.makedirs(os.path.join(OUTPUT_PATH, "trafilatura"), exist_ok=True)
    os.makedirs(os.path.join(DIFF_PATH, "trafilatura"), exist_ok=True)

    for idx, result in tqdm(enumerate(results), desc="Writing results"):
        with open(os.path.join(OUTPUT_PATH, "trafilatura", html_data[idx][0].replace(".html", ".txt")), "w") as f:
            print(result, file=f)

        with open(os.path.join(EXPECTED_PATH, "trafilatura", html_data[idx][0].replace(".html", ".txt")), "r") as expected_f, \
            open(os.path.join(DIFF_PATH, "trafilatura", html_data[idx][0].replace(".html", ".diff")), "w") as diff_f:
            expected = expected_f.read().rstrip('\n')
            
            if result != expected:
                diffs = compare(result, expected)
                print(diffs, file=diff_f)
            else:
                print("No differences found.", file=diff_f)
            
            assert result == expected, f"Failed on {html_data[idx][0]}"