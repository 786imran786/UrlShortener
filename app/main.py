from fastapi import HTTPException
from fastapi.responses import RedirectResponse

@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.long_url)
