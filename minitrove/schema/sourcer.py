import uuid

from pydantic import BaseModel


class Document(BaseModel):
    id: str | uuid.UUID
    text: str
    metadata: dict = {}