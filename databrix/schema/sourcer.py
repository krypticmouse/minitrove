import uuid

from pydantic import BaseModel


class Document(BaseModel):
    id: str | uuid.UUID | int
    text: str
    metadata: dict = {}