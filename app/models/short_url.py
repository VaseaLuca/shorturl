from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.dependencies.database import Base

class ShortURL(Base):
    __tablename__ = 'short_urls'
  
    id = Column(Integer, primary_key=True, autoincrement=True)
    shortcode = Column(String(50), unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_redirect = Column(DateTime(timezone=True), server_default=func.now())
    redirect_count = Column(Integer, default=0)