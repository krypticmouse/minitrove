import os
import fsspec

from tqdm import tqdm
from abc import abstractmethod
from typing import Dict, List, Tuple, Iterator
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from databrix.types import DocumentSource
from databrix.schema.sourcer import Document
from databrix.sourcer.utils import fetch_csv_schema, get_compression


class BaseSourcer:
    def __init__(
        self, 
        text_key: str,
        id_key: str,
        env_vars: Dict[str, str] | None = None,
        exclude_keys: List[str] | None = None,
    ):
        self.env_vars = env_vars
        self.text_key = text_key
        self.id_key = id_key
        self.exclude_keys = exclude_keys

        # Set keys as env variables
        if self.env_vars:
            for key, value in self.env_vars.items():
                os.environ[key] = value


    def source(
        self,
        path: str | List[str],
        compression: str | None = None,
        num_threads: int = 1,
        num_processes: int = 1,
    ) -> DocumentSource:
        if compression=="auto":
            compression = get_compression(path)

        if isinstance(path, str):
            return self.source_path(path, compression=compression, num_threads=num_threads)
        elif isinstance(path, list):
            return self.source_batch(path, compression=compression, num_threads=num_threads, num_processes=num_processes) 
        else:
            raise ValueError(f"Invalid path type: {type(path)}")


    @abstractmethod
    def fetch_document(self, idx: int, line: str) -> Tuple[int, Document]:
        raise NotImplementedError("Subclasses must implement fetch_document")


    def source_path(self, path: str, compression: str | None = None, num_threads: int = 1) -> Iterator[Document, None, None]:
        documents = []

        if ".csv" in path or ".tsv" in path:
            sep = "," if ".csv" in path else "\t"
            self.schema = fetch_csv_schema(path, sep=sep)


        with fsspec.open(path, compression=compression) as f:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(self.fetch_document, i, line) for i, line in enumerate(f)]
                documents = [None] * len(futures)

                for future in tqdm(as_completed(futures), desc="Processing documents"):
                    i, doc = future.result()
                    documents[i] = doc

        return documents



    def source_batch(
        self,
        paths: List[str],
        compression: str | None = None,
        num_threads: int = 1,
        num_processes: int = 1,
    ) -> List[Iterator[Document, None, None]]:
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(self.source_path, path, compression=compression, num_threads=num_threads) for path in tqdm(paths, desc="Sourcing documents")]

            documents = [future.result() for future in tqdm(futures, desc="Processing results")]

        return documents
