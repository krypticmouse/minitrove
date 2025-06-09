from typing import Iterator, List, TypeAlias

from databrix.schema.sourcer import Document


DocumentSource: TypeAlias = Iterator[Document] | List[Iterator[Document]]