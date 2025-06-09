from typing import Tuple
from trafilatura import extract
from resiliparse.extract.html2text import extract_plain_text

from databrix.extract.base import BaseExtractor
from databrix.schema.extract import ResiliparseConfig, TrafilaturaConfig


class ResiliparseExtractor(BaseExtractor):
    def __init__(self, config: ResiliparseConfig):
        super().__init__(config)


    def extract_text(self, idx: int, data: str) -> Tuple[int, str]:
        return idx, extract_plain_text(
            data,
            **self.config.model_dump()
        )


class TrafilaturaExtractor(BaseExtractor):
    def __init__(self, config: TrafilaturaConfig):
        super().__init__(config)


    def extract_text(self, idx: int, data: str) -> Tuple[int, str]:
        return idx, extract(
            data,
            **self.config.model_dump()
        )
