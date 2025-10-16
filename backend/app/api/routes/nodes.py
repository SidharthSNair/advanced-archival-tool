# # backend/app/api/routes/nodes.py
# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.orm import Session
# from typing import Optional
# from datetime import datetime, timedelta, timezone
#
# from app.db.session import SessionLocal
# from app.models import Node
# from app.schemas import NodePageOut
#
# router = APIRouter(prefix="/nodes", tags=["nodes"])
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @router.get("/", response_model=NodePageOut)
# def list_nodes(
#     share_id: int,
#     parent_id: Optional[int] = None,
#     # pagination
#     limit: int = Query(200, ge=1, le=1000),
#     offset: int = Query(0, ge=0),
#     # filters
#     q: Optional[str] = Query(None, description="substring match on name"),
#     kind: str = Query("all", pattern="^(all|file|dir)$"),
#     mtime_from: Optional[datetime] = None,
#     mtime_to: Optional[datetime] = None,
#     size_min: Optional[int] = Query(None, ge=0),
#     size_max: Optional[int] = Query(None, ge=0),
#     days_ago: Optional[int] = Query(None, ge=0, description="Show items not modified in the last X days"),
#     db: Session = Depends(get_db),
# ):
#     qset = db.query(Node).filter(Node.share_id == share_id)
#
#     # root vs children
#     if parent_id is None:
#         qset = qset.filter(Node.parent_id.is_(None))
#     else:
#         qset = qset.filter(Node.parent_id == parent_id)
#
#     # name contains
#     if q:
#         qset = qset.filter(Node.name.ilike(f"%{q}%"))
#
#     # kind filter
#     if kind == "file":
#         # keep folders at root so you can still navigate to files; only filter to files within children
#         if parent_id is not None:
#             qset = qset.filter(Node.is_dir.is_(False))
#     elif kind == "dir":
#         qset = qset.filter(Node.is_dir.is_(True))
#
#     # time filters
#     if mtime_from:
#         qset = qset.filter(Node.modified_at >= mtime_from)
#     if mtime_to:
#         qset = qset.filter(Node.modified_at <= mtime_to)
#     if days_ago is not None:
#         cutoff = datetime.now(timezone.utc) - timedelta(days=days_ago)
#         qset = qset.filter(Node.modified_at <= cutoff)
#
#     # size
#     if size_min is not None:
#         qset = qset.filter(Node.size >= size_min)
#     if size_max is not None:
#         qset = qset.filter(Node.size <= size_max)
#
#     qset = qset.order_by(Node.is_dir.desc(), Node.name.asc())
#
#     # pagination with "one extra" to detect more
#     rows = qset.limit(limit + 1).offset(offset).all()
#     has_more = len(rows) > limit
#     items = rows[:limit]
#
#     return {"items": items, "next_offset": (offset + limit) if has_more else None}


# Second Version

# backend/app/api/routes/nodes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, timezone

from app.db.session import SessionLocal
from app.models import Node
from app.schemas import NodePageOut

router = APIRouter(prefix="/nodes", tags=["nodes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=NodePageOut)
def list_nodes(
    share_id: int,
    parent_id: Optional[int] = None,
    # pagination
    limit: int = Query(200, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    # filters
    q: Optional[str] = Query(None, description="substring match on name"),
    kind: str = Query("all", pattern="^(all|file|dir)$"),
    mtime_from: Optional[datetime] = None,
    mtime_to: Optional[datetime] = None,
    size_min: Optional[int] = Query(None, ge=0),
    size_max: Optional[int] = Query(None, ge=0),
    days_ago: Optional[int] = Query(None, ge=0, description="Show items not modified in the last X days"),
    db: Session = Depends(get_db),
):
    qset = db.query(Node).filter(Node.share_id == share_id)

    # root vs children
    if parent_id is None:
        qset = qset.filter(Node.parent_id.is_(None))
    else:
        qset = qset.filter(Node.parent_id == parent_id)

    # name contains
    if q:
        qset = qset.filter(Node.name.ilike(f"%{q}%"))

    # kind filter
    if kind == "file":
        # keep folders at root so you can still navigate to files; only filter to files within children
        if parent_id is not None:
            qset = qset.filter(Node.is_dir.is_(False))
    elif kind == "dir":
        qset = qset.filter(Node.is_dir.is_(True))

    # time filters
    if mtime_from:
        qset = qset.filter(Node.modified_at >= mtime_from)
    if mtime_to:
        qset = qset.filter(Node.modified_at <= mtime_to)
    if days_ago is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_ago)
        qset = qset.filter(Node.modified_at <= cutoff)

    # size
    if size_min is not None:
        qset = qset.filter(Node.size >= size_min)
    if size_max is not None:
        qset = qset.filter(Node.size <= size_max)

    qset = qset.order_by(Node.is_dir.desc(), Node.name.asc())

    # pagination with "one extra" to detect more
    rows = qset.limit(limit + 1).offset(offset).all()
    has_more = len(rows) > limit
    items = rows[:limit]

    return {"items": items, "next_offset": (offset + limit) if has_more else None}
