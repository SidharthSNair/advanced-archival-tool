from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Node

router = APIRouter(prefix="/nodes", tags=["nodes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_nodes(share_id: int, parent_id: int | None = None, db: Session = Depends(get_db)):
    """List children nodes under a parent (or root if parent_id is None)."""
    q = db.query(Node).filter(Node.share_id == share_id)
    if parent_id is None:
        q = q.filter(Node.parent_id.is_(None))
    else:
        q = q.filter(Node.parent_id == parent_id)
    return q.all()
