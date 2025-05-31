import os

from tqdm import tqdm
from trafilatura import extract
from resiliparse.extract.html2text import extract_plain_text


INPUT_PATH = "tests/fixtures/extract/html"
OUTPUT_PATH = "tests/fixtures/extract/expected"


def generate_resiliparse_testset():
    for file in tqdm(os.listdir(INPUT_PATH)):
        if file.endswith(".html"):
            html_file = os.path.join(INPUT_PATH, file)
            text_file = os.path.join(OUTPUT_PATH, "resiliparse", file.replace(".html", ".txt"))

            html = open(html_file, "r").read()
            
            text = extract_plain_text(
                html,
                preserve_formatting=True,
                main_content=True,
            )
            
            with open(text_file, "w") as f:
                print(text, file=f)


def generate_trafilatura_testset():
    for file in tqdm(os.listdir(INPUT_PATH)):
        if file.endswith(".html"):
            html_file = os.path.join(INPUT_PATH, file)
            text_file = os.path.join(OUTPUT_PATH, "trafilatura", file.replace(".html", ".txt"))
            
            html = open(html_file, "r").read()
            text = extract(html, favor_recall=True)

            with open(text_file, "w") as f:
                print(text, file=f)


if __name__ == "__main__":
    generate_resiliparse_testset()
    generate_trafilatura_testset()