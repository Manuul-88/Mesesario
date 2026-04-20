import os
from pathlib import Path

import cloudinary
import cloudinary.uploader
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import MemoryMonth
from .schemas import MemoryMonthOut

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
STATIC_DIR = PROJECT_ROOT / "frontend" / "static"

app = FastAPI(title="Mesesario con BD")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://jessymanuel.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_upload(file: UploadFile | None):
    if not file or not file.filename:
        return None

    result = cloudinary.uploader.upload(
        file.file,
        folder="mesesario"
    )

    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id"),
    }


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/months", response_model=list[MemoryMonthOut])
def get_months(db: Session = Depends(get_db)):
    months = (
        db.query(MemoryMonth)
        .order_by(MemoryMonth.sort_order.asc(), MemoryMonth.id.asc())
        .all()
    )
    return months


@app.post("/api/months", response_model=MemoryMonthOut)
def create_month(
    month_label: str = Form(...),
    description: str = Form(...),
    is_featured: bool = Form(False),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    next_order = (db.query(MemoryMonth).count() or 0) + 1
    uploaded = save_upload(image)

    if is_featured:
        db.query(MemoryMonth).update({MemoryMonth.is_featured: False})

    month = MemoryMonth(
        month_label=month_label,
        description=description,
        image_path=uploaded["url"] if uploaded else None,
        image_public_id=uploaded["public_id"] if uploaded else None,
        is_featured=is_featured,
        sort_order=next_order,
    )

    db.add(month)
    db.commit()
    db.refresh(month)
    return month

@app.put("/api/months/{month_id}", response_model=MemoryMonthOut)
def update_month(
    month_id: int,
    month_label: str = Form(...),
    description: str = Form(...),
    is_featured: bool = Form(False),
    keep_existing_image: bool = Form(True),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    month = db.query(MemoryMonth).filter(MemoryMonth.id == month_id).first()
    if not month:
        raise HTTPException(status_code=404, detail="Mes no encontrado")

    if is_featured:
        db.query(MemoryMonth).update({MemoryMonth.is_featured: False})

    month.month_label = month_label
    month.description = description
    month.is_featured = is_featured

    if image and image.filename:
        if month.image_public_id:
            cloudinary.uploader.destroy(month.image_public_id)

        uploaded = save_upload(image)
        month.image_path = uploaded["url"] if uploaded else None
        month.image_public_id = uploaded["public_id"] if uploaded else None

    elif not keep_existing_image:
        if month.image_public_id:
            cloudinary.uploader.destroy(month.image_public_id)

        month.image_path = None
        month.image_public_id = None

    db.commit()
    db.refresh(month)
    return month

@app.delete("/api/months/{month_id}")
def delete_month(month_id: int, db: Session = Depends(get_db)):
    month = db.query(MemoryMonth).filter(MemoryMonth.id == month_id).first()
    if not month:
        raise HTTPException(status_code=404, detail="Mes no encontrado")

    if month.image_public_id:
        cloudinary.uploader.destroy(month.image_public_id)

    db.delete(month)
    db.commit()

    ordered = (
        db.query(MemoryMonth)
        .order_by(MemoryMonth.sort_order.asc(), MemoryMonth.id.asc())
        .all()
    )

    for index, item in enumerate(ordered, start=1):
        item.sort_order = index

    db.commit()
    return {"ok": True}