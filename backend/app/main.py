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
        "https://mesesario-beta.vercel.app",
        "https://mesesario-bgxsc7ue4-manul-88s-projects.vercel.app",
    ],
    allow_credentials=False,
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


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "on"}


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
    description_1: str = Form(""),
    description_2: str = Form(""),
    is_featured: str = Form("false"),
    image_1: UploadFile | None = File(None),
    image_2: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    is_featured_bool = parse_bool(is_featured)

    next_order = (db.query(MemoryMonth).count() or 0) + 1

    uploaded_1 = save_upload(image_1) if image_1 else None
    uploaded_2 = save_upload(image_2) if image_2 else None

    if is_featured_bool:
        db.query(MemoryMonth).update({MemoryMonth.is_featured: False})


    month = MemoryMonth(
    month_label=month_label,
    description=description_1 or description_2 or "",
    description_1=description_1,
    image_path_1=uploaded_1["url"] if uploaded_1 else None,
    image_public_id_1=uploaded_1["public_id"] if uploaded_1 else None,
    description_2=description_2,
    image_path_2=uploaded_2["url"] if uploaded_2 else None,
    image_public_id_2=uploaded_2["public_id"] if uploaded_2 else None,
    is_featured=is_featured_bool,
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
    description_1: str = Form(""),
    description_2: str = Form(""),
    is_featured: str = Form("false"),
    keep_existing_image_1: str = Form("true"),
    keep_existing_image_2: str = Form("true"),
    image_1: UploadFile | None = File(None),
    image_2: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    month = db.query(MemoryMonth).filter(MemoryMonth.id == month_id).first()
    if not month:
        raise HTTPException(status_code=404, detail="Mes no encontrado")

    is_featured_bool = parse_bool(is_featured)
    keep_existing_1_bool = parse_bool(keep_existing_image_1)
    keep_existing_2_bool = parse_bool(keep_existing_image_2)

    if is_featured_bool:
        db.query(MemoryMonth).update({MemoryMonth.is_featured: False})

    month.month_label = month_label
    month.description_1 = description_1
    month.description_2 = description_2
    month.is_featured = is_featured_bool

    if image_1 and image_1.filename:
        if month.image_public_id_1:
            cloudinary.uploader.destroy(month.image_public_id_1)
        uploaded_1 = save_upload(image_1)
        month.image_path_1 = uploaded_1["url"] if uploaded_1 else None
        month.image_public_id_1 = uploaded_1["public_id"] if uploaded_1 else None
    elif not keep_existing_1_bool:
        if month.image_public_id_1:
            cloudinary.uploader.destroy(month.image_public_id_1)
        month.image_path_1 = None
        month.image_public_id_1 = None

    if image_2 and image_2.filename:
        if month.image_public_id_2:
            cloudinary.uploader.destroy(month.image_public_id_2)
        uploaded_2 = save_upload(image_2)
        month.image_path_2 = uploaded_2["url"] if uploaded_2 else None
        month.image_public_id_2 = uploaded_2["public_id"] if uploaded_2 else None
    elif not keep_existing_2_bool:
        if month.image_public_id_2:
            cloudinary.uploader.destroy(month.image_public_id_2)
        month.image_path_2 = None
        month.image_public_id_2 = None

    db.commit()
    db.refresh(month)
    return month


@app.delete("/api/months/{month_id}")
def delete_month(month_id: int, db: Session = Depends(get_db)):
    month = db.query(MemoryMonth).filter(MemoryMonth.id == month_id).first()
    if not month:
        raise HTTPException(status_code=404, detail="Mes no encontrado")

    if month.image_public_id_1:
        cloudinary.uploader.destroy(month.image_public_id_1)

    if month.image_public_id_2:
        cloudinary.uploader.destroy(month.image_public_id_2)

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