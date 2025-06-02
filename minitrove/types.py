from typing import Iterator, List, TypeAlias

from minitrove.schema.sourcer import Document


DocumentSource: TypeAlias = Iterator[Document] | List[Iterator[Document]]