from pydantic import BaseModel

class MemoryMonthOut(BaseModel):
    id: int
    month_label: str

    description: str | None = None
    image_path: str | None = None
    image_public_id: str | None = None

    description_1: str | None = None
    image_path_1: str | None = None
    image_public_id_1: str | None = None

    description_2: str | None = None
    image_path_2: str | None = None
    image_public_id_2: str | None = None

    is_featured: bool
    sort_order: int

    class Config:
        from_attributes = True