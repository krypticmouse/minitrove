from pydantic import BaseModel
from typing import Any, List, Optional, Dict

class BaseExtractionConfig(BaseModel):
    pass


class ResiliparseConfig(BaseExtractionConfig):
    preserve_formatting: bool = True
    main_content: bool = True



class TrafilaturaConfig(BaseExtractionConfig):
    favor_recall: bool = True