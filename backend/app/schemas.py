#formato de la respuesta
from pydantic import BaseModel


class MemoryMonthOut(BaseModel):
    id: int
    month_label: str
    description: str
    image_path: str | None = None
    is_featured: bool
    sort_order: int

    class Config:
        from_attributes = True