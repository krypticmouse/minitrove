from tqdm import tqdm
from typing import Any, List, Tuple
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor

from databrix.schema.extract import BaseExtractionConfig


class BaseExtractor(ABC):
    def __init__(self, config: BaseExtractionConfig):
        self.config = config


    @abstractmethod
    def extract_text(self, idx: int, data: str) -> Tuple[int, str]:
        pass
 

    def extract(self, data: List[str], num_workers: int = 1) -> Any:
        results = [None] * len(data)

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self.extract_text, idx, data) for idx, data in tqdm(enumerate(data), desc="Extracting text")]

            for future in tqdm(futures, desc="Processing results"):
                index, result = future.result()
                results[index] = result
        
        return results
