from pydantic import BaseModel

class DocumentSection(BaseModel):
    department: str
    title: str
    content: str
    source: str  # File name or section reference