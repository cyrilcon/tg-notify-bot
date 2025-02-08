from pydantic import BaseModel, Field, ConfigDict


class Document(BaseModel):
    buffer: bytes = Field(..., description="Byte buffer of the document")
    name: str = Field(..., description="Name of the document")
