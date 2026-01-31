from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import URL
from .utils import encode_base62

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/shorten")
def shorten_url(long_url: str, db: Session = Depends(get_db)):
    url = URL(long_url=long_url)
    db.add(url)
    db.commit()
    db.refresh(url)

    short_code = encode_base62(url.id)
    url.short_code = short_code
    db.commit()

    return {"short_url": f"http://localhost:8000/{short_code}"}

from fastapi import HTTPException
from fastapi.responses import RedirectResponse

@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    if short_code == "favicon.ico":
        raise HTTPException(status_code=204)

    try:
        cached = r.get(short_code)
    except:
        cached = None

    if cached:
        return RedirectResponse(cached)

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    try:
        r.set(short_code, url.long_url)
    except:
        pass

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.long_url)
