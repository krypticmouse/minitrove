import uuid
import fsspec
import orjson

from tqdm import tqdm
from typing import Iterator, Tuple

from databrix.schema.sourcer import Document
from databrix.sourcer.base import BaseSourcer
from concurrent.futures import ThreadPoolExecutor, as_completed


class JSONSourcer(BaseSourcer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = None

    def fetch_document(self, idx: int, line: str) -> Tuple[int, Document]:
        data = orjson.loads(line)

        if self.exclude_keys:
            data = {k: v for k, v in data.items() if k not in self.exclude_keys}
        
        return idx, Document(
            id=data[self.id_key],
            text=data[self.text_key],
            metadata=data,
        )
    

class CSVSourcer(BaseSourcer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sep = ","

    def fetch_document(self, idx: int, line: str) -> Tuple[int, Document]:
        row = line.split(self.sep)
        data = {k: row[self.schema[k]] for k in self.schema.keys()}
        return idx, Document(
            id=data[self.id_key],
            text=data[self.text_key],
            metadata=data,
        )


class TSVSourcer(CSVSourcer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sep = "\t"


class TXTSourcer(BaseSourcer):
    def __init__(self, split_by_newline: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.split_by_newline = split_by_newline


    def fetch_document(self, idx: int, line: str) -> Tuple[int, Document]:
        return idx, Document(
            id=uuid.uuid4(),
            text=line,
        )

    def source_path(self, path: str, compression: str | None = None, num_threads: int = 1) -> Iterator[Document]:
        documents = []

        if self.split_by_newline:
            with fsspec.open(path, compression=compression) as f:
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    futures = [executor.submit(self.fetch_document, i, line) for i, line in enumerate(f)]
                    documents = [None] * len(futures)

                    for future in tqdm(as_completed(futures), desc="Processing documents"):
                        i, doc = future.result()
                        documents[i] = doc
        else:
            with fsspec.open(path, compression=compression) as f:
                text = f.read()
                documents = [Document(id=uuid.uuid4(), text=text.strip())]

        return documents 
