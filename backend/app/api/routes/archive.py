from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz

from app.db.session import SessionLocal
from app.models import ArchiveRequest
from app.core.config import settings

router = APIRouter(prefix="/archive", tags=["archive"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def next_saturday_10am_est():
    """Compute next Saturday 10 AM EST from now."""
    tz = pytz.timezone(settings.SCHED_TZ)
    now = datetime.now(tz)
    days_until_sat = (5 - now.weekday()) % 7  # Saturday = weekday 5
    next_sat = now + timedelta(days=days_until_sat)
    return tz.localize(datetime.combine(next_sat.date(), datetime.min.time())) + timedelta(hours=10)


@router.post("/")
def schedule_archive(payload: dict, db: Session = Depends(get_db)):
    """
    payload = {
      "region_code": "NA",
      "location_code": "HFX",
      "share_unc": "\\\\hfxshare\\dept1",
      "paths": [ "C:/folder1", "C:/folder2" ]
    }
    """
    required = ["region_code", "location_code", "share_unc", "paths"]
    if not all(k in payload for k in required):
        raise HTTPException(status_code=400, detail="Missing required fields")

    req = ArchiveRequest(
        region_code=payload["region_code"],
        location_code=payload["location_code"],
        share_unc=payload["share_unc"],
        paths_json={"paths": payload["paths"]},
        scheduled_est=next_saturday_10am_est(),
        status="pending",
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    return {
        "message": "Archive scheduled successfully",
        "scheduled_for": req.scheduled_est.isoformat(),
        "id": req.id,
    }


@router.get("/")
def list_requests(db: Session = Depends(get_db)):
    """View all archive requests (for testing/admin)."""
    return db.query(ArchiveRequest).order_by(ArchiveRequest.created_at.desc()).all()
