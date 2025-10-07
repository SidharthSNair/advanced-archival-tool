from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Region, Location, Share




router = APIRouter(prefix="/regions", tags=["regions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()

@router.get("/{region_code}/locations")
def list_locations(region_code: str, db: Session = Depends(get_db)):
    return db.query(Location).filter(Location.region_code == region_code).all()

@router.get("/locations/{location_code}/shares")
def list_shares(location_code: str, db: Session = Depends(get_db)):
    # First, get the location by code
    location = db.query(Location).filter(Location.code == location_code).first()
    if not location:
        return []  # or raise HTTPException(status_code=404, detail="Location not found")

    # Then, filter shares by location_id (not location_code)
    return db.query(Share).filter(Share.location_id == location.id).all()


@router.get("/ping")
def ping():
    return {"status": "regions router is active"}
