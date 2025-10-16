from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# --- Read models
class RegionOut(BaseModel):
    code: str
    name: str

    class Config: from_attributes = True


class LocationOut(BaseModel):
    id: int
    code: str
    name: str
    region_code: str

    class Config: from_attributes = True


class ShareOut(BaseModel):
    id: int
    unc_path: str
    location_id: int

    class Config: from_attributes = True


class NodeOut(BaseModel):
    id: int
    name: str
    path: str
    is_dir: bool
    size: int
    modified_at: datetime
    parent_id: Optional[int] = None
    share_id: int

    class Config:
        from_attributes = True


class NodePageOut(BaseModel):
    items: List[NodeOut]
    next_offset: Optional[int] = None


# --- Archive
class ArchiveIn(BaseModel):
    region_code: str = Field(min_length=1, max_length=16)
    location_code: str = Field(min_length=1, max_length=64)
    share_unc: str = Field(min_length=1, max_length=512)
    paths: List[str] = Field(min_items=1)


class ArchiveOut(BaseModel):
    id: int
    message: str
    scheduled_for: datetime
