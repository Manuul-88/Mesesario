from sqlalchemy import Boolean, Column, Integer, String, Text
from .database import Base

class MemoryMonth(Base):
    __tablename__ = "memory_months"

    id = Column(Integer, primary_key=True, index=True)
    month_label = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(500), nullable=True)
    image_public_id = Column(String(255), nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)