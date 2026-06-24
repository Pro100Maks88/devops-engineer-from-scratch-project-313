from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class LinkBase(SQLModel):
    original_url: str
    short_name: str

class LinkCreate(LinkBase):
    pass

class LinkRead(LinkBase):
    id: int
    created_at: datetime
    short_url: str

    @staticmethod
    def from_orm(link, base_url: str) -> "LinkRead":
        return LinkRead(
            id=link.id,
            original_url=link.original_url,
            short_name=link.short_name,
            created_at=link.created_at,
            short_url=f"{base_url.rstrip('/')}/r/{link.short_name}",
        )

class Link(LinkBase, table=True):
    __tablename__ = "links"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

