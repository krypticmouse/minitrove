from pydantic import BaseModel
from typing import Any, List, Optional, Dict

class BaseExtractionConfig(BaseModel):
    pass


class ResiliparseConfig(BaseExtractionConfig):
    preserve_formatting: bool = True
    main_content: bool = True

    alt_texts: bool = True
    links: bool = False
    form_fields: bool = False
    noscript: bool = False
    comments: bool = True
    post_meta: bool = True
    hidden_elements: bool = False
    skip_elements: Optional[List[str]] = None


class TrafilaturaConfig(BaseExtractionConfig):
    favor_recall: bool = True
    favor_precision: bool = False
    output_format: str = 'txt'
    
    target_language: str | None = None
    include_tables: bool = True
    include_images: bool = False
    include_formatting: bool = False
    include_links: bool = False
    include_comments: bool = True

    url: str | None = None
    record_id: str | None = None
    fast: bool = False
    no_fallback: bool = False
    tei_validation: bool = False
    deduplicate: bool = False
    date_extraction_params: Optional[Dict[str, Any]] = None
    with_metadata: bool = False
    only_with_metadata: bool = False
    max_tree_size: int | None = None
    url_blacklist: set[str] | None = None
    author_blacklist: set[str] | None = None
    settingsfile: str | None = None
    prune_xpath: Any | None = None
    config: Any = None
    options: Any | None = None
