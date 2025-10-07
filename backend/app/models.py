from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base

# --- Region (e.g., NA, Asia, Europe)
class Region(Base):
    __tablename__ = "regions"

    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    locations: Mapped[list["Location"]] = relationship(back_populates="region")

# --- Location (e.g., Halifax, Tokyo, Frankfurt)
class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    region_code: Mapped[str] = mapped_column(ForeignKey("regions.code"), index=True)
    region: Mapped["Region"] = relationship(back_populates="locations")

    shares: Mapped[list["Share"]] = relationship(back_populates="location")

# --- Share (file share UNC path or mount)
class Share(Base):
    __tablename__ = "shares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unc_path: Mapped[str] = mapped_column(String(512), unique=True, index=True)

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), index=True)
    location: Mapped["Location"] = relationship(back_populates="shares")

    nodes: Mapped[list["Node"]] = relationship(back_populates="share")

# --- Node (file or folder in the share)
class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    path: Mapped[str] = mapped_column(String(2048), index=True)
    is_dir: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(Integer, default=0)
    modified_at: Mapped[datetime] = mapped_column(DateTime, index=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("nodes.id"), nullable=True)
    share_id: Mapped[int] = mapped_column(ForeignKey("shares.id"), index=True)

    parent: Mapped["Node"] = relationship(remote_side=[id])
    share: Mapped["Share"] = relationship(back_populates="nodes")

# --- Archive Requests (scheduling deletions/moves)
class ArchiveRequest(Base):
    __tablename__ = "archive_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_code: Mapped[str] = mapped_column(String(16), index=True)
    location_code: Mapped[str] = mapped_column(String(32), index=True)
    share_unc: Mapped[str] = mapped_column(String(512), index=True)

    # List of selected paths (as JSON array)
    paths_json: Mapped[dict] = mapped_column(JSON)

    scheduled_est: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    result_message: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
