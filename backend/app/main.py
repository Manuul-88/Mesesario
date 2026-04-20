import shutil
import uuid
from pathlib import Path

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
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Mesesario con BD")

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

print("STATIC_DIR =", STATIC_DIR)
print("EXISTE STATIC_DIR =", STATIC_DIR.exists())

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_upload(file: UploadFile | None) -> str | None:
    if not file or not file.filename:
        return None

    suffix = Path(file.filename).suffix.lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/uploads/{filename}"


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
    image_path = save_upload(image)

    if is_featured:
        db.query(MemoryMonth).update({MemoryMonth.is_featured: False})

    month = MemoryMonth(
        month_label=month_label,
        description=description,
        image_path=image_path,
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
        month.image_path = save_upload(image)
    elif not keep_existing_image:
        month.image_path = None

    db.commit()
    db.refresh(month)
    return month


@app.delete("/api/months/{month_id}")
def delete_month(month_id: int, db: Session = Depends(get_db)):
    month = db.query(MemoryMonth).filter(MemoryMonth.id == month_id).first()
    if not month:
        raise HTTPException(status_code=404, detail="Mes no encontrado")

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