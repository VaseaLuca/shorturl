import re
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from app.dependencies.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.short_url import ShortURL
from pydantic import BaseModel
import random
import string

router = APIRouter()

def get_session_local():
    yield SessionLocal()

class CreateShortUrlRequestBase(BaseModel):
    url: str
    shortcode: str = None

@router.post("/shorten")
def create_short_url(short_url_req: CreateShortUrlRequestBase, db: Session = Depends(get_session_local)):

    if not short_url_req.url:
        raise HTTPException(status_code=400, detail="Url not present")
    
    if not short_url_req.shortcode:
        length = 6
        characters = string.ascii_letters + string.digits + "_"
        shortcode = "".join(random.choice(characters) for _ in range(length))
        
    else:
        if db.query(ShortURL).filter(ShortURL.shortcode == short_url_req.shortcode).first():
            raise HTTPException(status_code=409, detail="Shortcode already in use")
        
        if not re.match(r'^[a-zA-Z0-9_]{6,}$', short_url_req.shortcode):
            raise HTTPException(status_code=412, detail="The provided shortcode is invalid")
        
        shortcode = short_url_req.shortcode
        
    short_url = ShortURL(shortcode=shortcode, original_url= short_url_req.url)
    
    db.add(short_url)
    db.commit()
    
    return JSONResponse(status_code=201, content={"shortcode": shortcode})

@router.get("/{shortcode}")
def redirect_to_original_url(shortcode: str, db: Session = Depends(get_session_local)):
    short_url = db.query(ShortURL).filter(ShortURL.shortcode == shortcode).first()
    
    if not short_url:
        raise HTTPException(status_code=404, detail="Shortcode not found")

    short_url.redirect_count += 1
    db.commit()

    return RedirectResponse(url=short_url.original_url, status_code=302)

@router.get("/{shortcode}/stats")
def get_stats(shortcode: str, db: Session = Depends(get_session_local)):
    short_url = db.query(ShortURL).filter(ShortURL.shortcode == shortcode).first()
    
    if not short_url:
        raise HTTPException(status_code=404, detail="Shortcode not found")
    
    created = short_url.created_at.isoformat()
    last_redirect = short_url.last_redirect.isoformat()
    
    return JSONResponse(status_code=200, content={
        "created": created,
        "lastRedirect": last_redirect,
        "redirectCount": short_url.redirect_count
    })